all: run-dev

run-dev:
	poetry run python bot/xeltbot.py

pyright:
	poetry run pyright bot
