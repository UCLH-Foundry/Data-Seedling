.PHONY: help

define all-pipelines  # Arguments: <command>
	find . -maxdepth 1 -mindepth 1 -type d | xargs -i bash -c 'if [ -f "{}/pipeline.json" ]; then echo {}; fi' | xargs -i make -C {} $(1)
endef


help: ## Show this help
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%s\033[0m|%s\n", $$1, $$2}' \
        | column -t -s '|'
	@echo

artifacts: ## Create all pipeline artifacts
	$(call all-pipelines,artifacts)

install-all: install-build install-test install-lint

install-build: ## Install all pre-requisites for build for all pipelines
	$(call all-pipelines,install-build)

install-test: ## Install all pre-requisites for test for all pipelines
	$(call all-pipelines,install-test)

install-lint: ## Install all pre-requisites for lint for all pipelines
	$(call all-pipelines,install-lint)

test: ## Test all pipelines
	$(call all-pipelines,test)

mypy: ## Call mypy on all pipelines
	$(call all-pipelines,mypy)