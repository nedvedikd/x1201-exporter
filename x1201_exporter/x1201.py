import struct
from dataclasses import dataclass

import gpiod
import smbus2
from gpiod.line import Direction


@dataclass
class BatteryReading:
    voltage: float
    capacity: float


class X1201Metrics:
    _address: int
    _pld_line: int
    _bus: smbus2.SMBus

    def __init__(self) -> None:
        self._address = 0x36
        self._pld_line = 6
        self._bus = smbus2.SMBus(1)

    def _read_word_data(self, register: int) -> int:
        return self._bus.read_word_data(self._address, register)

    def read_battery(self) -> BatteryReading:
        voltage_read = self._read_word_data(2)
        capacity_read = self._read_word_data(4)

        [voltage_swapped] = struct.unpack("<H", struct.pack(">H", voltage_read))
        [capacity_swapped] = struct.unpack("<H", struct.pack(">H", capacity_read))

        # X1201 is using MAX17043 chip for determining battery state
        # the formula below converts the raw I2C reading to the actual voltage
        # - each LSB in the reading represents 1.25mV (from the MAX17043 datasheet)
        # - multiply by 1.25 to get the value in millivolts
        # - divide by 1000 to convert millivolts to volts
        # - divide by 16 - this is a tricky part, I'm not sure why there is a x16 scaling factor
        voltage = voltage_swapped * 1.25 / 1000 / 16
        capacity = capacity_swapped / 256

        battery_reading = BatteryReading(voltage=voltage, capacity=capacity)

        return battery_reading

    def get_power_state(self) -> int:
        config = {self._pld_line: gpiod.LineSettings(direction=Direction.INPUT)}

        with gpiod.request_lines(
            path="/dev/gpiochip4",
            consumer="PLD",
            config=config,
        ) as request:
            return request.get_value(self._pld_line).value
