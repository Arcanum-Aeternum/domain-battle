test:
	pytest

style:
	black ./ --line-length=120
	isort ./
