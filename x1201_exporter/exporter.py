import random

from fastapi import FastAPI, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    CollectorRegistry,
    Gauge,
    generate_latest,
)

app = FastAPI()

registry = CollectorRegistry()

TEST_GAUGE = Gauge("x1201_test", "Testing X1201 Metric", registry=registry)


def update_metrics() -> None:
    TEST_GAUGE.set(random.randint(1, 100))


@app.get("/metrics")
def metrics():
    update_metrics()
    metrics_data = generate_latest(registry)
    return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)
