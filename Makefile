.PHONY: all run test reports notebooks venv clean

all: run test

run:
	python3 -m scripts.run_notebooks && python3 -m scripts.build_reports

test:
	python3 -m unittest discover -s tests -v

reports:
	python3 -m scripts.build_reports

notebooks:
	python3 -m scripts.run_notebooks

venv:
	python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

clean:
	rm -rf __pycache__ .ipynb_checkpoints *.egg-info
