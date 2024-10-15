# This Makefile helps perform some developer tasks, like linting or testing.
# Run `make` or `make help` to see a list of tasks.
# Based on GCOVR project (https://github.com/gcovr/gcovr).

PYTHON_VERSION ?= 3.7

ATLASSIAN_SDK ?= atlassian-sdk
QA_CONTAINER ?= atlassian-python-api-qa-$(PYTHON_VERSION)
TEST_OPTS ?=

LINTING_TARGETS := atlassian/ examples/ tests/

.PHONY: help setup-dev qa lint test doc docker-qa docker-qa-build

help:
	@echo "select one of the following targets:"
	@echo "  help       print this message"
	@echo "  setup-dev  prepare a development environment"
	@echo "  qa         run all QA tasks"
	@echo "  test       run the tests"
	@echo "  docker-qa  run qa in the docker container"
	@echo "  docker-qa-build"
	@echo "             build the qa docker container"
	@echo ""
	@echo "environment variables:"
	@echo "  TEST_OPTS  additional flags for pytest [current: $(TEST_OPTS)]"
	@echo "  QA_CONTAINER"
	@echo "             tag for the qa docker container [current: $(QA_CONTAINER)]"

setup-dev:
	python3 -m pip install --upgrade pip pytest
	python3 -m pip install -r requirements-dev.txt

qa: tox

tox: export PYTHONDONTWRITEBYTECODE := 1

tox:
	tox

docker-qa: export TEST_OPTS := $(TEST_OPTS)
docker-qa: export PYTHONDONTWRITEBYTECODE := 1

docker-qa: | docker-qa-build
	docker run --rm -e TEST_OPTS -e PYTHONDONTWRITEBYTECODE -v `pwd`:/atlassian-python-api $(QA_CONTAINER)

docker-qa-build: Dockerfile.qa requirements.txt requirements-dev.txt
	docker build \
		--tag $(QA_CONTAINER) \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--file $< .

docker-fmt: docker-qa-build
	docker run --rm -v `pwd`:/atlassian-python-api $(QA_CONTAINER) tox -e black_fmt

docker-atlassian-standalone: Dockerfile.standalone
	docker build \
		--tag $(ATLASSIAN_SDK) \
		--file $< .
