SHELL := /bin/bash

VENV := .venv
PYTHON := python3
REQS := requirements.txt
APP := src/app.py
DOWNLOAD := src/setup/download

.PHONY: run
run: setup
	@source $(VENV)/bin/activate && \
	textual run --dev $(APP)

.PHONY: web
web: setup
	@source $(VENV)/bin/activate && \
	textual serve --dev --host 0.0.0.0 --port 8000 $(APP)

.PHONY: setup
setup: $(VENV)
	@source $(VENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r $(REQS)
	chmod +x $(DOWNLOAD)/download_smogon.sh
	./$(DOWNLOAD)/download_smogon.sh

# Create virtual environment if missing
$(VENV):
	$(PYTHON) -m venv $(VENV)
