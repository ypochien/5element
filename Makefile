typehint:
	mypy 5element/ tests/

test:
	pytest tests/

lint:
	pylint 5element/ tests/

checklist:	lint typehint test

.PHONY:	all