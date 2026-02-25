.PHONY: setup run test format lint clean

# Default python command
PYTHON = venv/bin/python
UVICORN = venv/bin/uvicorn
PIP = venv/bin/pip

setup:
	python3 -m venv venv
	$(PIP) install -r requirements.txt
	@echo "Setup complete. Be sure to fill out your .env file."

run:
	$(UVICORN) app.main:app --host 127.0.0.1 --port 8000 --reload

deps:
	docker compose up -d

down:
	docker compose down

clean:
	rm -rf venv
	rm -rf __pycache__
	rm -rf .pytest_cache

# Example commands for linting / testing (assume installed later)
# format:
# 	$(PYTHON) -m black .
#
# lint:
# 	$(PYTHON) -m flake8 .
#
# test:
# 	$(PYTHON) -m pytest
