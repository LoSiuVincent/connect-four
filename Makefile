RUN = poetry run

run-dev:
	$(RUN) uvicorn connect_four.main:app --reload --host 0.0.0.0 --port 8000