# x1201-exporter

Lightweight Prometheus Metrics Exporter for the X1201 UPS HAT for Raspberry Pi 5

Exports 3 metrics:
 - Battery Voltage (`x1201_battery_voltage`)
 - Battery Capacity (`x1201_battery_capacity`)
 - Power State (`x1201_power_state`)


## Example with Prometheus

docker-compose.yml:
```
services:
  x1201-exporter:
    image: nedvedikd/x1201-exporter:1.0.0
    container_name: x1201-exporter
    restart: unless-stopped
    privileged: true
    devices:
      - "/dev/i2c-1:/dev/i2c-1:ro"
      - "/dev/gpiochip4:/dev/gpiochip4:ro"

  prometheus:
    image: prom/prometheus
    container_name: prometheus
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
    restart: unless-stopped

volumes:
  prometheus_data:
    driver: local
```

prometheus/prometheus.yml:
```
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'x1201-exporter'
    scrape_interval: 5s
    static_configs:
      - targets: ['x1201-exporter:80']
```
