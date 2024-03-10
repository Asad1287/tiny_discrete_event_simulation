.PHONY: install test clean simple_test

install:
	pip install -e .
	pip install -r requirements.txt

test:
	pytest

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache

simple_test:
	python -m samples.simple_des

simple_test2:
	python -m samples.simple_des
