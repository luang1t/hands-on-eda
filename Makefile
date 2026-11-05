PYTHON ?= $(shell if [ -f .venv/bin/python ]; then echo .venv/bin/python; else echo python3; fi)

.PHONY: all run test reports notebooks venv clean

all: run test

run:
	$(PYTHON) -m scripts.run_notebooks && $(PYTHON) -m scripts.build_reports

test:
	$(PYTHON) -m unittest discover -s tests -v

reports:
	$(PYTHON) -m scripts.build_reports

notebooks:
	$(PYTHON) -m scripts.run_notebooks

venv:
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

clean:
	find . -type d \( -name __pycache__ -o -name .ipynb_checkpoints -o -name "*.egg-info" -o -name ".pytest_cache" \) -exec rm -rf {} +
	rm -rf .test_*
