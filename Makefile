.PHONY: lint test build clean install

lint:
	ruff check --fix

test:
	python -m unittest discover -s tests

build:
	python setup.py sdist bdist_wheel

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf dist build *.egg-info

install:
	pip install .
