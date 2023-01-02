all: run-dev

run-dev:
	poetry run python bot/xelt.py

mypy:
	poetry run mypy bot