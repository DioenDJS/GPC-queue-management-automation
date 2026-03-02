VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip

venv:
	python3.12 -m venv $(VENV)
	$(PIP) install --upgrade pip

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) main.py

format:
	ruff check --select I --fix
	ruff format