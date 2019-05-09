## help:      print this help message and exit
help: Makefile
	@echo ''
	@sed -n 's/^## //p' Makefile
	@echo ''

## test:      execute the automated test suite
test:
	pytest --cov=rsidx --doctest-modules rsidx/*/test_*.py

## devdeps:   install development dependencies
devdeps:
	pip install --upgrade pip setuptools
	pip install wheel twine
	pip install pycodestyle pytest-cov pytest-sugar


## devhooks:  install development hooks
devhooks:
	echo 'set -eo pipefail' > .git/hooks/pre-commit
	echo 'make style' >> .git/hooks/pre-commit
	chmod 755 .git/hooks/pre-commit

## clean:     remove development artifacts
clean:
	rm -rf __pycache__/ rsidx/__pycache__/ rsidx/*/__pycache__ build/ dist/ *.egg-info/

## style:     check code style against PEP8
style:
	pycodestyle rsidx/*.py rsidx/*/*.py
