#  Copyright (c) University College London Hospitals NHS Foundation Trust
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

.PHONY: help

help: ## Show this help
	@echo
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%s\033[0m|%s\n", $$1, $$2}' \
        | column -t -s '|'
	@echo

install: ## Installs the required dependencies	

build: ## Build the Python wheel(s)

artifacts: ## Gather artifacts for sending to Spark
	mkdir -p artifacts
	cp helloworld.py artifacts

clean: ## Clean all built objects
	rm -r artifacts

test: ## Run unit tests

mypy: ## Run mypy (see https://jaredkhan.com/blog/mypy-pre-commit on why it isn't run in pre-commit hook)

lint: ## Run pre-commit checks
