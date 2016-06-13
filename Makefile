
default: deps

deps: annotran.egg-info/.uptodate node_modules/.uptodate

annotran.egg-info/.uptodate: setup.py requirements.txt
	pip install --use-wheel -e .[dev,testing,YAML]
	touch $@

node_modules/.uptodate: package.json
	npm install
	touch $@

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf annotran/static/webassets-external
	rm -f annotran/static/scripts/vendor/*.min.js
	rm -f annotran/static/scripts/account.*js
	rm -f annotran/static/scripts/app.*js
	rm -f annotran/static/scripts/config.*js
	rm -f annotran/static/scripts/hypothesis.*js
	rm -f annotran/static/styles/*.css
	rm -f .coverage
	rm -f node_modules/.uptodate .eggs/.uptodate

dev: deps
	@gunicorn --reload --paste development.ini

test: backend-test

backend-test:
	py.test -q