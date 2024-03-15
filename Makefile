.PHONY: init
init:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements-dev.txt
	test -f config.json || cp config.example.json config.json

.PHONY: lint
lint:
	black .
	flake8 .
	isort .
	mypy .

.PHONY: run
run:
	python main.py -c default
