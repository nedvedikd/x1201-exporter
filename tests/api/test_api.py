import urllib.parse

import pytest
import requests

BASE_URL = "http://localhost:8080"


@pytest.mark.api
def test_metrics_endpoint() -> None:
    endpoint = "/metrics"
    url = urllib.parse.urljoin(BASE_URL, endpoint)

    response = requests.get(url)

    assert response.status_code == 200

    body = response.text

    assert "x1201_battery_voltage" in body
    assert "x1201_battery_capacity" in body
    assert "x1201_power_state" in body
