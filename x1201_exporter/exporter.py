from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST

from x1201_exporter.metrics_manager import X1201PrometheusMetricsManager

app = FastAPI()
metrics_manager = X1201PrometheusMetricsManager()


@app.get("/metrics")
async def metrics():
    metrics_data = metrics_manager.get_metrics()
    return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)
