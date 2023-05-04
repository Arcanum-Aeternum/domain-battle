test:
	pytest -s -l -vvv domain/

test-cov:
	pytest -s -l -vvv domain/ --cov domain/ --cov-fail-under=85 --cov-report term:skip-covered

style:
	black ./ --line-length=120
	isort ./

check-code:
	isort --check-only domain/ \
	&& black --check domain/ \
	&& mypy domain/ \
	&& pylint domain/
