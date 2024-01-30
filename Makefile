RUN = poetry run

run-dev:
	$(RUN) uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

all-test: unit-test integration-test functional-test

unit-test:
	npm test tests/javascripts/unit

integration-test:
	pytest tests/test_integrations.py
	npm test tests/javascripts/integration.test.js

functional-test:
	pytest tests/test_functionals.py

update-baseline:
	UPDATE_BASELINE=1 pytest -m visual

linter:
	poetry run autoflake -i -r .
	poetry run isort .
	poetry run black .