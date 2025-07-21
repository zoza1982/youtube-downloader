.PHONY: help install install-dev test test-cov lint format clean build upload-test upload

help:
	@echo "YouTube Downloader CLI - Development Commands"
	@echo "============================================"
	@echo ""
	@echo "install       Install package in development mode"
	@echo "install-dev   Install all development dependencies"
	@echo "test          Run tests"
	@echo "test-cov      Run tests with coverage report"
	@echo "lint          Run code linting (flake8)"
	@echo "format        Format code with black"
	@echo "clean         Clean build artifacts"
	@echo "build         Build distribution packages"
	@echo "upload-test   Upload to TestPyPI"
	@echo "upload        Upload to PyPI"

install:
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest

test-cov:
	pytest --cov=ytd --cov-report=term-missing --cov-report=html

lint:
	flake8 ytd/ tests/ --max-line-length=120

format:
	black ytd/ tests/

type-check:
	mypy ytd/

quality: format lint type-check test

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

build: clean
	python setup.py sdist bdist_wheel

upload-test: build
	twine upload --repository testpypi dist/*

upload: build
	twine upload dist/*