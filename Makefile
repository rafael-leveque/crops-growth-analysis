
.venv:
	### Check prerequisites and install .venv ###

	# Check prerequisites
	@which pyenv || (echo "Please install pyenv first. Check README.md." && exit 1)
	@pyenv version || pyenv install || (echo "Cannot install python version. Check README.md." && exit 1)

	# Install and create venv
	@pip install virtualenv
	@python -m venv .venv

.PHONY: install

install: .venv
	### Install requirements ###
	@.venv/bin/python -m pip install -q --upgrade pip
	@.venv/bin/pip install -q -r requirements.txt

.PHONY: run

run: install
	### Run the application ###
	@.venv/bin/python crops-growth-analysis/main.py