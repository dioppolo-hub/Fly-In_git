PYTHON := python3

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) Simulation.py

debug:
	$(PYTHON) -m pdb Simulation.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .mypy_cache

lint: mypy flake8

lint-strict: lint
	mypy . --strict

flake8:
	flake8 .

mypy:
	mypy . --warn-return-any \
	--warn-unused-ignores \
	--ignore-missing-imports \
	--disallow-untyped-defs \
	--check-untyped-defs

.PHONY: lint mypy flake8 run clean