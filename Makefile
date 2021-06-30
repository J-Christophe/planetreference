.DEFAULT_GOAL := init
.PHONY: prepare-dev install-dev data help lint tests coverage upload-prod-pypi upload-test-pypi doc doc-pdf visu-doc-pdf visu-doc tox licences
VENV = ".planetreference"

define PROJECT_HELP_MSG

Usage:\n
	\n
    make help\t\t\t             show this message\n
	\n
	-------------------------------------------------------------------------\n
	\t\tInstallation\n
	-------------------------------------------------------------------------\n
	make\t\t\t\t                Install planetreference in the system (root)\n
	make user\t\t\t 			Install planetreference for non-root usage\n
	\n
	-------------------------------------------------------------------------\n
	\t\tDevelopment\n
	-------------------------------------------------------------------------\n
	make prepare-dev\t\t 		Prepare Development environment\n
	make install-dev\t\t 		Install COTS and planetreference for development purpose\n
	make data\t\t\t				Download data\n
	make test\t\t\t             Run units and integration tests\n
	\n
	make doc\t\t\t 				Generate the documentation\n
	make doc-pdf\t\t\t 			Generate the documentation as PDF\n
	make visu-doc-pdf\t\t 		View the generated PDF\n
	make visu-doc\t\t\t			View the generated documentation\n
	\n
	make release\t\t\t 			Release the package as tar.gz\n
	make upload-test-pypi\t\t   Upload the pypi package on the test platform\n
	make upload-prod-pypi\t\t   Upload the pypi package on the prod platform\n
	\n
	-------------------------------------------------------------------------\n
	\t\tOthers\n
	-------------------------------------------------------------------------\n
	make licences\t\t	Display the list of licences\n
	make version\t\t	Display the version\n
	make coverage\t\t 	Coverage\n
	make lint\t\t		Lint\n
	make tox\t\t 		Run all tests\n

endef
export PROJECT_HELP_MSG


#Show help
#---------
help:
	echo $$PROJECT_HELP_MSG


#
# Sotware Installation in the system (need root access)
# -----------------------------------------------------
#
init:
	python3 setup.py install

#
# Sotware Installation for user
# -----------------------------
# This scheme is designed to be the most convenient solution for users
# that don’t have write permission to the global site-packages directory or
# don’t want to install into it.
#
user:
	python3 setup.py install --user

prepare-dev:
	cp .pypirc ~${USER} && git init && echo "python3 -m venv planetreference-env && export PYTHONPATH=. && export PATH=`pwd`/planetreference-env/bin:${PATH}" > ${VENV} && echo "source \"`pwd`/planetreference-env/bin/activate\"" >> ${VENV} && scripts/install-hooks.bash && echo "\nnow source this file: \033[31msource ${VENV}\033[0m"

install-dev:
	pip install -r requirements.txt && pip install -r requirements_dev.txt && pre-commit install && pre-commit autoupdate && python3 setup.py develop

coverage:  ## Run tests with coverage
	coverage erase
	coverage run --include=planetreference/* -m pytest -ra
	coverage report -m

lint:  ## Lint and static-check
	flake8 --ignore=E203,E266,E501,W503,F403,F401 --max-line-length=79 --max-complexity=18 --select=B,C,E,F,W,T4,B9 planetreference
	pylint planetreference
	mypy planetreference

tests:  ## Run tests
	pytest -ra

tox:
	tox -e py37

doc:
	make html -C docs

doc-pdf:
	make doc && make latexpdf -C docs

visu-doc-pdf:
	make doc-pdf && acroread docs/build/latex/planetreference.pdf

visu-doc:
	make doc && firefox docs/build/html/index.html

release:
	python3 setup.py sdist

version:
	python3 setup.py --version

data:
	pip install -r requirements_data.txt && python scripts/data_download.py

upload-test-pypi:
	flit publish --repository pypitest

upload-prod-pypi:
	flit publish

licences:
	pip-licenses