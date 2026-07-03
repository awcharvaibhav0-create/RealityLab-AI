.PHONY: setup run test lint clean docker-build docker-run

setup:
	pip install -r requirements.txt
	python -m pytest --version || pip install pytest

run:
	streamlit run frontend/app.py

test:
	pytest tests/ -v

lint:
	flake8 .
	mypy .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

docker-build:
	docker-compose build

docker-run:
	docker-compose up -d
