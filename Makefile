

.venv:
	pip install virtualenv
	venv .venv
	.venv/bin/activate


install: .venv
	.venv/bin/pip install -r requirements.txt