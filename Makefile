RUN = poetry run

run-dev:
	$(RUN) uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

all-test: unit-test integration-test functional-test

unit-test:
	npm test tests/frontend/unit

integration-test:
	$(RUN) pytest tests/test_integrations.py
	npm test tests/frontend/integration.test.js

functional-test:
	$(RUN) pytest tests/test_functionals.py

update-baseline:
	rm tests/baseline/*
	UPDATE_BASELINE=1 $(RUN) pytest -m visual

linter:
	poetry run autoflake -i -r .
	poetry run isort .
	poetry run black .