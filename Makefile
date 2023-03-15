.PHONY: build clean clean-docker clean-docs docs help repl test shell start stop lint migrate migrations dev-tools-check lint-tools-check poetry
.DEFAULT_GOAL: help

# define standard colors
ifneq ($(TERM),)
    GREEN        := $(shell tput setaf 2)
    RESET        := $(shell tput sgr0)
else
    GREEN        := ""
    RESET        := ""
endif

REPORT := $(or $(REPORT),report -m)
GIT_CHANGED_PYTHON_FILES := $(shell git diff --name-only -- '***.py')
LINTING_TOOLS := $(and $(shell which black),$(shell which isort),$(shell which flake8))
DEV_TOOLS := $(shell which docker compose)
CONTAINER := $(or $(CONTAINER),elixir)

help:
	@echo "${GREEN}+--------------------------------------------------------------------------------+${RESET}"
	@echo "${GREEN}| Elixir: itrax                                                                  |${RESET}"
	@echo "${GREEN}+--------------------------------------------------------------------------------+${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| Description:                                                                   |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| Assists in working with itrax by placing common functionality in one file      |${RESET}"
	@echo "${GREEN}| much of the usage is combined in few rules that can be customized via          |${RESET}"
	@echo "${GREEN}| command line arguments.                                                        |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| The test rule has three arguments src, test-case and report, these args        |${RESET}"
	@echo "${GREEN}| allow a developer to test in various ways (see below) and get reports in       |${RESET}"
	@echo "${GREEN}| different ways too.                                                            |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| help: Prints this message                                                      |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| run: Runs the application                                                      |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| lint: Lints python code                                                        |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| stop: Stops the application                                                    |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| migrations: Creates the django migrations                                      |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| migrate: Applies the django migrations                                         |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}| test: Runs tests                                                               |${RESET}"
	@echo "${GREEN}|       SRC:       The source folder to limit coverage to (optional)             |${RESET}"
	@echo "${GREEN}|       TEST-CASE: The tests to run, may be one or many (optional)               |${RESET}"
	@echo "${GREEN}|       REPORT:    The type of report to generate (optional)                     |${RESET}"
	@echo "${GREEN}|                  Please see coverage.py help for more info                     |${RESET}"
	@echo "${GREEN}| https://coverage.readthedocs.io/en/latest/cmd.html?highlight=report#reporting  |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       Examples:                                                                |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       1. To run all tests parallelised:                                        |${RESET}"
	@echo "${GREEN}|          make test                                                             |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       2. To run a subset of tests with coverage of a specific folder:          |${RESET}"
	@echo "${GREEN}|          make test SRC=trs/ TEST-CASE=itracker.trs.tests                       |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       3. To run a subset of tests with full coverage:                          |${RESET}"
	@echo "${GREEN}|          make test SRC=. TEST-CASE=itracker.trs.tests                          |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       4. To run all tests with coverage generated as html:                     |${RESET}"
	@echo "${GREEN}|          make test SRC=. REPORT=html                                           |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       5. To run all tests with coverage generated in console (default)         |${RESET}"
	@echo "${GREEN}|          make test SRC=. REPORT=report -m                                      |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       6. To run all tests with coverage generated in xml                       |${RESET}"
	@echo "${GREEN}|          make test SRC=. REPORT=xml                                            |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       7. To run all tests with coverage generated in json                      |${RESET}"
	@echo "${GREEN}|          make test SRC=. REPORT=json                                           |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       8. To run all tests with coverage generated in lcov                      |${RESET}"
	@echo "${GREEN}|          make test SRC=. REPORT=lcov                                           |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       9. To run a subset of tests parallelised:                                |${RESET}"
	@echo "${GREEN}|          make test TEST-CASE=itracker.trs.tests                                |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}|       Note - Coverage does not currently work correctly with                   |${RESET}"
	@echo "${GREEN}|              parallelisation. Also, TEST-CASE can be a subset of tests         |${RESET}"
	@echo "${GREEN}|              or even a single unit test.                                       |${RESET}"
	@echo "${GREEN}|                                                                                |${RESET}"
	@echo "${GREEN}+--------------------------------------------------------------------------------+${RESET}"

dev-tools-check:
ifeq ($(DEV_TOOLS),)
	$(error Some of your dev tools are missing, unable to proceed)
endif

lint-tools-check:
ifeq ($(LINTING_TOOLS),)
	$(error Some of your linting tools are missing, unable to proceed)
endif

build: dev-tools-check
ifeq ($(FORCE),true)
	@docker container rm -f $(CONTAINER)
	@docker container prune
endif
	@docker compose build $(CONTAINER)

start: dev-tools-check
	@docker compose up $(CONTAINER) --remove-orphans

stop: dev-tools-check
	@docker compose stop $(CONTAINER)

lint: lint-tools-check
	@$(foreach file, $(GIT_CHANGED_PYTHON_FILES), $(shell black ${file}; isort ${file}; flake8 ${file}))

migrate: dev-tools-check
	@docker compose run --rm $(CONTAINER) poetry run python ./manage.py migrate

migrations: dev-tools-check
	@docker compose run --rm $(CONTAINER) poetry run python ./manage.py makemigrations $(ARGS)

repl: dev-tools-check
	@docker compose run --rm $(CONTAINER) poetry run python manage.py shell

shell:
	@docker compose run --rm $(CONTAINER) /bin/bash

test: dev-tools-check
	@rm -rf coverage
ifneq ($(and $(TEST-CASE),$(SRC)),)
	@docker compose run --rm $(CONTAINER) coverage run --source=$(SRC) --branch ./manage.py test --no-input $(TEST-CASE); docker-compose run --rm $(CONTAINER) coverage $(REPORT)
else ifneq ($(SRC),)
	@docker compose run --rm $(CONTAINER) coverage run --source=$(SRC) --branch ./manage.py test --no-input; docker-compose run --rm $(CONTAINER) coverage $(REPORT)
else ifneq ($(TEST-CASE),)
	@docker compose run --rm $(CONTAINER) coverage run --branch ./manage.py test --no-input $(TEST-CASE) --parallel
else
	@docker compose run --rm $(CONTAINER) coverage run --branch ./manage.py test --no-input --parallel
endif
	@rm -rf .coverage.*

clean-docker:
	@docker volume prune -f
	@docker image prune -f
	@docker system prune -f

clean-docs:
	@rm -rf docs/build

clean: clean-docker clean-docs

docs: dev-tools-check
	@docker compose run --rm $(CONTAINER) poetry run sphinx-apidoc -f -o docs/source/ . ./*/test/*.py ./tests/*.py ./*/migrations/*.py ./*/tests/*.py ./settings/environments/*.py ./settings/*.py ./debug_snippet.py ./scinamic/update_compounds_from_scinamic.py
	@cd docs && make html CONTAINER=$(CONTAINER)

poetry:

	@docker compose run --rm $(CONTAINER) poetry $(CMD)
