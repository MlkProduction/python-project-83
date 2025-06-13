install:
		uv sync

dev:
		uv run flask --debug --app page_analyzer:app run

PORT ?= 8000
start:
		uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
		./build.sh

render-start:
		venv/bin/python -m gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

lint:
		uv run ruff check page_analyzer

fix-lint:
		uv run ruff check --fix page_analyzer  

test:
		PYTHONPATH=$(PWD) uv run pytest -vv

test-coverage:
		uv run pytest --cov=gendiff --cov-report xml

check: test lint