.PHONY: lint test build clean install

lint:
	ruff check --fix

test:
	python -m unittest discover -s tests

build:
	python setup.py sdist bdist_wheel

clean:
	rm -rf dist build *.egg-info

install:
	pip install .
