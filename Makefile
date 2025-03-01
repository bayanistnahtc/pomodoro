.DEFAULT_GOAL := help

run: ## Run the app using uvicorn
	python -m poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload --env-file .local.env

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	python -m poetry add $(LIBRARY)

uninstall: ## Uninstalling a dependency using poetry
	@echo "Uninstalling dependency ${LIBRARY}"
	python -m poetry remoce ${LIBRARY}


help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:
	@echo -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %\n", $$1, $$2}'