typehint:
	mypy src/ tests/

test:
	pytest tests/

lint:
	pylint src/ tests/

checklist:	lint typehint test

.PHONY:	all