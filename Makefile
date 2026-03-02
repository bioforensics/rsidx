## help:      print this help message and exit
help: Makefile
	@echo ''
	@sed -n 's/^## //p' Makefile
	@echo ''

## test:      execute the automated test suite
test:
	pytest --cov=rsidx --doctest-modules rsidx/*/test_*.py

## style:     check code style
style:
	black --line-length=99 --check rsidx/*.py rsidx/*/*.py

## format:    autoformat Python code
format:
	black --line-length=99 rsidx/*.py rsidx/*/*.py

## hooks:     install development hooks
hooks:
	echo 'set -eo pipefail' > .git/hooks/pre-commit
	echo 'make style' >> .git/hooks/pre-commit
	chmod 755 .git/hooks/pre-commit
