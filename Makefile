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

.PHONY: gen_migration
gen_migration:
	alembic revision --autogenerate -m "${NAME}"

.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: migrate_history
migrate_history:
	alembic history

.PHONY: rollback
rollback:
	alembic downgrade -1
