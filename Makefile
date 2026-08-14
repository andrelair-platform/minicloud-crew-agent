.PHONY: lint fmt test test-cov run

lint:
	ruff check app/ tests/
	ruff format --check app/ tests/
	mypy app/

fmt:
	ruff format app/ tests/
	ruff check --fix app/ tests/

test:
	pytest tests/unit/ -q

test-cov:
	pytest tests/unit/ --cov=app --cov-report=term-missing --cov-fail-under=70

run:
	uvicorn app.main:app --host 0.0.0.0 --port 8081 --reload
