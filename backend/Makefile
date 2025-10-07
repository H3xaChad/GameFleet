dev:
	uv run uvicorn gamefleet.main:app --reload --host 127.0.0.1 --port 8000

start:
	uv run uvicorn gamefleet.main:app --host 0.0.0.0 --port 8000

migrate:
	uv run alembic upgrade head

createmigration:
	uv run alembic revision --autogenerate

automigrate:
	uv run sh -c 'alembic revision --autogenerate && alembic upgrade head'
