SHELL=/bin/bash

SRC_DIR = src
CONF_FILE := production.ini

help: ## this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {sub("\\\\n",sprintf("\n%22c"," "), $$2);printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

dev-install: ## installs dependencies in the dev profile
	pip install -e '$(SRC_DIR)[dev]'

dev-server: ini/development.ini ## run the development server
	PYRAMID_RELOAD_TEMPLATES=1 pserve 'ini/development.ini' --reload

test:
	python -m unittest discover src

clean: ## removes all the python bytecode and cache files
	find $(SRC_DIR) -name \*.pyc -print -delete
	find $(SRC_DIR) -name __pycache__ -print -delete

.PHONY: clean help \
	dev-server dev-install \
