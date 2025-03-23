.DEFAULT_GOAL := help

run: ## Run the app using uvicorn
	poetry run gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 4 -c gunicorn.conf.py


install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)


uninstall: ## Uninstalling a dependency using poetry
	@echo "Uninstalling dependency ${LIBRARY}"
	poetry remove ${LIBRARY}


help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:
	@echo -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %\n", $$1, $$2}'


migrate-create:
	alembic revision --autogenerate -m ${MIGRATION}


migrate-apply:
	alembic upgrade head
