import urllib.parse

import requests

BASE_URL = "http://localhost:8000"


def test_metrics_endpoint() -> None:
    endpoint = "/metrics"
    url = urllib.parse.urljoin(BASE_URL, endpoint)

    response = requests.get(url)

    assert response.status_code == requests.codes.get("✓")

    body = response.text

    assert "x1201_battery_voltage" in body
    assert "x1201_battery_capacity" in body
    assert "x1201_power_state" in body
