RUN = poetry run
BASELINE_DIR = tests/functional/baseline
CURRENT_DIR = tests/functional/current

run-dev:
	$(RUN) uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-level 'info'

run-prod:
	$(RUN) uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level 'info'

all-test: clean-current unit-test integration-test functional-test

unit-test:
	npm test tests/frontend/unit
	$(RUN) pytest tests/backend/unit

integration-test:
	npm test tests/frontend/integration.test.js
	$(RUN) pytest tests/backend/integration

functional-test:
	$(RUN) pytest tests/functional/test_functionals.py

clean-current:
	rm -r $(CURRENT_DIR)
	mkdir $(CURRENT_DIR)

update-baseline:
	rm -r $(BASELINE_DIR)
	mkdir $(BASELINE_DIR)
	UPDATE_BASELINE=1 $(RUN) pytest -m visual

linter:
	poetry run autoflake -i -r .
	poetry run isort .
	poetry run black .
	poetry run flake8 src tests
	poetry run vulture src tests