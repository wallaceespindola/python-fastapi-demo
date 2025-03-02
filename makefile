.PHONY: install install-dep venv activate deactivate test run pre-commit build updates version help

# ATTENTION: It must be TABS AND NOT SPACES before the commands, otherwise it will not work.

install:
	pip install -e .

install-dep:
	pip install -r requirements.txt

venv:
	python -m venv .venv

activate:
	source .venv/bin/activate

deactivate:
	deactivate

test:
	pytest --verbose

run:
	python -m python-fastapi-demo

pre-commit:
	pre-commit run --all-files

build:
	rm -rf ./dist
	python -m build

updates:
	pip list -o

version:
	python-fastapi-demo -v

help:
	python-fastapi-demo -h

# USAGE:
# make install
# make install-dep
# make venv
# make activate
# make deactivate
# make test
# make run
# make pre-commit
# make build
# make updates
# make version
# make help
