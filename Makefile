# Common tasks for the Endeavours CMS.
# Run `make help` for the list.

PYTHON := .venv/bin/python
PIP    := .venv/bin/pip
MANAGE := $(PYTHON) manage.py

.DEFAULT_GOAL := help
.PHONY: help venv install install-prod env migrate migrations superuser run \
        seed css css-watch static test lint format check clean reset-db

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-16s\033[0m %s\n", $$1, $$2}'

venv: ## Create the virtualenv
	python3.12 -m venv .venv

install: venv ## Install dev dependencies (Python + Node)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements/dev.txt
	npm install

install-prod: ## Install production Python dependencies
	$(PIP) install -r requirements/production.txt

env: ## Create .env from the example if it does not exist
	@test -f .env || (cp .env.example .env && echo "Created .env - edit it before running.")

migrations: ## Generate migrations
	$(MANAGE) makemigrations

migrate: ## Apply migrations
	$(MANAGE) migrate

superuser: ## Create an admin user
	$(MANAGE) createsuperuser

seed: ## Load demo navigation, footer and page content
	$(MANAGE) seed_demo_content

run: ## Start the development server
	$(MANAGE) runserver

css: ## Build the stylesheet once (minified)
	npm run build

css-watch: ## Rebuild the stylesheet on change
	npm run dev

static: ## Collect static files for deployment
	$(MANAGE) collectstatic --noinput

test: ## Run the test suite
	$(PYTHON) -m pytest

lint: ## Check formatting and lint rules
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .

format: ## Apply formatting and autofixes
	.venv/bin/ruff check --fix .
	.venv/bin/ruff format .

check: ## Run Django system checks
	$(MANAGE) check

clean: ## Remove build artefacts and caches
	find . -path ./.venv -prune -o -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .ruff_cache staticfiles

reset-db: ## Drop and recreate the local database, then migrate and seed
	dropdb --if-exists wagtail_cms
	createdb wagtail_cms
	$(MANAGE) migrate
	$(MANAGE) seed_demo_content
