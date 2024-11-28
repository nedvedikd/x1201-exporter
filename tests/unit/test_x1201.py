from x1201_exporter.x1201 import X1201Metrics


def test_read_battery(mocker) -> None:
    metrics = X1201Metrics()

    mock_values = {
        2: 20688,  # Voltage read value
        4: 32865,  # Capacity read value
    }

    mocker.patch.object(
        metrics, "_read_word_data", side_effect=lambda x: mock_values[x]
    )

    # Call the method under test
    battery_reading = metrics.read_battery()

    assert battery_reading.voltage == 4.16625
    assert battery_reading.capacity == 97.5
