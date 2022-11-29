.PHONY: fmt style tests app-local

fmt:
	poetry run isort .
	poetry run black .

style:
	poetry run isort --check --diff .
	poetry run black --check --diff .
	poetry run mypy -p app

tests:
	docker-compose down -v
	docker-compose up --build --remove-orphans -d database
	poetry run python -m pytest -s tests
	docker-compose down -v

app-local:
	docker-compose up --build --remove-orphans -d database
	poetry run alembic upgrade head
	export ENVIRONMENT=local
	poetry run uvicorn family_budget.app:app --reload
	docker-compose docker