.PHONY: install test test-api test-ui test-headed docker-build docker-test docker-test-api docker-test-ui clean

install:
	pip install -r requirements.txt
	playwright install chromium

test:
	pytest

test-api:
	pytest -m api

test-ui:
	pytest -m ui

test-headed:
	HEADLESS=false pytest -m ui

docker-build:
	docker compose build

docker-test:
	docker compose run --rm tests

docker-test-api:
	docker compose run --rm tests-api-only

docker-test-ui:
	docker compose run --rm tests-ui-only

clean:
	rm -rf reports/
	mkdir -p reports/screenshots
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
