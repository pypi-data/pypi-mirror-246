.SHELL := /bin/bash
.PHONY: all format lint test test-rs build-dev build-release profile type

all: lint format test test-rs
	@echo "All done!"

format:
	@echo "Running formatter..."
	isort .
	black .

lint:
	@echo "Running linter..."
	-ruff . --fix

test:
	@echo "Running tests..."
	-pytest -vs tests/
	
test-rs:
	@echo "Running tests..."
	-cargo test -- --nocapture

build-dev:
	@echo "Building dev..."
	-maturin develop --release

build-release:
	@echo "Building release..."
	-maturin build --release

profile:
	@echo "Profiling..."
	-python -m tests.profiler


type:
	@echo "Running type checker (pyright 1.1.340) ..."
	pyright src/