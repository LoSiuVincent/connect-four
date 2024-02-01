RUN = poetry run

run-dev:
	$(RUN) uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

all-test: clean-current unit-test integration-test functional-test

unit-test:
	npm test tests/frontend/unit

integration-test:
	$(RUN) pytest tests/test_integrations.py
	npm test tests/frontend/integration.test.js

functional-test:
	$(RUN) pytest tests/test_functionals.py

clean-current:
	rm -r tests/current
	mkdir tests/current

update-baseline:
	rm -r tests/baseline
	mkdir tests/baseline
	UPDATE_BASELINE=1 $(RUN) pytest -m visual

linter:
	poetry run autoflake -i -r .
	poetry run isort .
	poetry run black .
	poetry run flake8 src tests