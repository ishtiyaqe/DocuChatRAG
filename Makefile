.PHONY: up down build logs backend-shell createsuperuser test format

build:
\tdocker-compose build

up:
\tdocker-compose up -d

down:
\tdocker-compose down

logs:
\tdocker-compose logs -f --tail=200

backend-shell:
\tdocker-compose exec backend bash

createsuperuser:
\tdocker-compose exec backend python manage.py createsuperuser

test:
\t# minimal: ensure imports and migrations run
\tdocker-compose run --rm backend bash -lc "python manage.py check && python manage.py makemigrations --check --dry-run"

format:
\t# placeholder for your linters/formatters
\t@echo "Add black/isort/eslint here"
