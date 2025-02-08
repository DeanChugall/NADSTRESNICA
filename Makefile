.PHONY: clean all allp format quality test

#################################################################################
# SETUP                                                                         #
#################################################################################
setup:
	pip install -r requirements.txt

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	# delete all .pytest_cache
	find . -type d -name "*.pytest_cache" -exec rm -rf {} +
	# delete all .ruff_cache
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist
	rm -rf .ipynb_checkpoints
	rm -rf .coverage*

all:
	pre-commit run --all-files

allp:
	git add .
	pre-commit run

format:
	ruff format .
	ruff check --fix .

quality:
	ruff format --check .
	ruff check .

test:
	poetry run pytest -v -s
