.PHONY: test test-unit test-api build-dev-image run-dev stop-dev
.SILENT: test test-unit test-api build-dev-image run-dev stop-dev

test:
	pytest -v

test-unit:
	pytest -v -m unit

test-api:
	pytest -v -m api

build-dev-image:
	docker build -t nedvedikd/x1201-exporter:dev --target production .

run-dev: build-dev-image
	docker run -dp 8080:80 \
  		--name x1201-exporter-dev \
  		--restart unless-stopped \
  		--privileged \
  		--device /dev/i2c-1:/dev/i2c-1 \
  		--device /dev/gpiochip4:/dev/gpiochip4 \
  		nedvedikd/x1201-exporter:dev > /dev/null

stop-dev:
	docker container stop x1201-exporter-dev > /dev/null
	docker container rm x1201-exporter-dev > /dev/null
