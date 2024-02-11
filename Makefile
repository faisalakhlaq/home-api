.PHONY: seed test mypy migrations migrate collectstatic run_dev

## Backend-dev terminal
test:
	pytest -n auto apps

mypy:
	mypy --strict .

flake8: ## run flak8 check
	flake8;

migrations: ## Make django migration files
	python manage.py makemigrations;

migrate: ## Apply Django migrations
	python manage.py migrate;

collectstatic: ## Generate Django static files
	python manage.py collectstatic;

seed: ## Seed the database
	cat seed/local.py | python manage.py shell;

run_dev: ## Run the DEV server
	gunicorn --bind 0.0.0.0:8000 --reload balkan.wsgi --timeout 100000;

build_backend:
	docker compose build backend;

start_backend: ## Run backend and go to its shell
	docker compose run --service-ports backend;

prune: ## Prune volumes and containers
	make prune_volumes;
	make prune_local_volumes;
	make prune_containers;
	make prune_build;

prune_volumes: ## Prune volumes
	docker system prune --volumes;

prune_local_volumes: ## Prune all local unused volumes
	docker volume rm $(docker volume ls)

prune_containers: ## Prune all containers
	docker system prune -af;

prune_build: ## Remove all build cache without prompt for confirmation
	docker builder prune && docker builder prune -af;
