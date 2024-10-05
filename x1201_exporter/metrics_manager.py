from prometheus_client import CollectorRegistry, Gauge, generate_latest

from x1201_exporter.x1201 import X1201Metrics


class X1201PrometheusMetricsManager:
    _battery_voltage_gauge: Gauge
    _battery_capacity_gauge: Gauge
    _power_state_gauge: Gauge
    _x1201_metrics: X1201Metrics
    _registry: CollectorRegistry

    def __init__(self) -> None:
        self._registry = CollectorRegistry()
        self._battery_voltage_gauge = Gauge(
            "x1201_battery_voltage", "X1201 Battery Voltage", registry=self._registry
        )
        self._battery_capacity_gauge = Gauge(
            "x1201_battery_capacity", "X1201 Battery Capacity", registry=self._registry
        )
        self._power_state_gauge = Gauge(
            "x1201_power_state", "X1201 Power State", registry=self._registry
        )
        self._x1201_metrics = X1201Metrics()

    def _update_metrics(self) -> None:
        battery_reading = self._x1201_metrics.read_battery()
        self._battery_voltage_gauge.set(battery_reading.voltage)
        self._battery_capacity_gauge.set(battery_reading.capacity)

        power_state = self._x1201_metrics.get_power_state()
        self._power_state_gauge.set(power_state)

    def get_metrics(self) -> bytes:
        self._update_metrics()
        return generate_latest(self._registry)
