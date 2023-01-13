all: run-dev

run-dev:
	poetry run python bot/xeltbot.py

mypy:
	poetry run mypy bot

pyright:
	poetry run pyright bot

tests:
	poetry run pytest tests/redis --asyncio-mode auto