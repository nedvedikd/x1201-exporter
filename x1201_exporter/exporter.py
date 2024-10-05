from fastapi import FastAPI, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Gauge,
    generate_latest,
)

from x1201_exporter.x1201 import X1201Metrics

app = FastAPI()

registry = CollectorRegistry()

x1201_metrics = X1201Metrics()

X1201_BATTERY_VOLTAGE_GAUGE = Gauge(
    "x1201_battery_voltage", "X1201 Battery Voltage", registry=registry
)
X1201_BATTERY_CAPACITY_GAUGE = Gauge(
    "x1201_battery_capacity", "X1201 Battery Capacity", registry=registry
)


def update_metrics() -> None:
    battery_reading = x1201_metrics.read_voltage_and_capacity()

    X1201_BATTERY_VOLTAGE_GAUGE.set(battery_reading.voltage)
    X1201_BATTERY_CAPACITY_GAUGE.set(battery_reading.capacity)


@app.get("/metrics")
async def metrics():
    update_metrics()
    metrics_data = generate_latest(registry)
    return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)
