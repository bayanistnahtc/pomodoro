.DEFAULT_GOAL := help

run: ## Run the app using uvicorn
	poetry run gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --workers 4 -c infra/gunicorn.conf.py
	# poetry run gunicorn main:app --worker-class uvicorn.workers.UvicornWorker -c infra/gunicorn.conf.py

	# poetry run waitress-serve main:app  --listen=*:8000
	## -workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --env-file .local.env


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
