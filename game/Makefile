PYTHON_VERSION := 3.10
PYTHON_BIN := python$(PYTHON_VERSION)

VENV_DEV := .venv-dev
VENV := .venv

$(VENV_DEV):
	$(PYTHON_BIN) -m venv $(VENV_DEV); \
		. $(VENV_DEV)/bin/activate; \
		pip install --upgrade pip; \
		pip install -e .[dev];

.PHONY: setup-dev
setup-dev: $(VENV_DEV)

$(VENV):
	$(PYTHON_BIN) -m venv $(VENV); \
		. $(VENV)/bin/activate; \
		pip install --upgrade pip; \
		pip install -e .;

.PHONY: setup
setup: $(VENV)

.PHONY: clean
clean:
	rm -rf \
		$(VENV_DEV) \
		$(VENV)
