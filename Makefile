.DEFAULT_GOAL := all

.PHONY: all

all : clean install lint run

.venv:
	$(info ### Check prerequisites and install .venv ###)
	$(info )

	$(info # Check prerequisites)
	@which pyenv || (echo "Please install pyenv first. Check README.md." && exit 1)
	@pyenv version || pyenv install || (echo "Cannot install python version. Check README.md." && exit 1)
	$(info )

	$(info # Install and create venv)
	@pip install virtualenv
	@python -m venv .venv
	$(info )

.PHONY: install

install: .venv
	$(info ### Install requirements ###)
	@.venv/bin/python -m pip install -q --upgrade pip
	@.venv/bin/pip install -q -r requirements.txt
	$(info )

.PHONY: run

run: install
	$(info ### Run the application ###)
	@.venv/bin/python crops_growth_analysis/main.py
	$(info )

.PHONY: lint

lint: install
	$(info ### Run linter ###)
	@.venv/bin/pylint crops_growth_analysis
	@.venv/bin/mypy crops_growth_analysis
	@.venv/bin/flake8 crops_growth_analysis
	@.venv/bin/black crops_growth_analysis
	@.venv/bin/isort crops_growth_analysis
	$(info )

.PHONY: clean

clean:
	$(info ### Clean the project ###)
	@rm -rf .venv
	@rm -rf crops_growth_analysis/**/.mypy_cache
	@rm -rf crops_growth_analysis/**/__pycache__
	$(info )