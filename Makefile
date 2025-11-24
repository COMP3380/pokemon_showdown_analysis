VENV := .venv
PYTHON := python3
REQS := requirements.txt
APP := src/app/app.py

.PHONY: run
run: setup
	@source $(VENV)/bin/activate && \
	textual run --dev $(APP)

# Setup virtual environment and install dependencies
.PHONY: setup
setup: $(VENV)
	@source $(VENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r $(REQS)

# Create virtual environment if missing
$(VENV):
	$(PYTHON) -m venv $(VENV)
