pytest --ds=sq.settings --cov --cov-report=html:coverage_report/html --cov-report=term
flake8 *.py */*.py --max-line-length=120