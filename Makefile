# One entry point for all five stacks. Each target is independent, so you can
# bootstrap/run a single language or the whole portfolio.
#
#   make install     install deps for every stack
#   make test        run every suite
#   make smoke       run the fast smoke subset where a stack defines one
#   make py-test / js-test / java-test / newman / pact   run one stack
#   make clean       remove generated artifacts
#
# Java needs Maven + JDK 17; Newman target installs the newman CLI globally.

.PHONY: install test smoke clean \
        py-install py-test py-smoke \
        js-install js-test js-smoke \
        java-test java-smoke \
        newman pact

# ---- aggregate ------------------------------------------------------------
install: py-install js-install
	@echo "Java pulls its deps on first 'mvn test'; Newman installs in its target."

test: py-test js-test java-test newman pact

smoke: py-smoke js-smoke java-smoke

# ---- python-pytest --------------------------------------------------------
py-install:
	cd python-pytest && pip install -r requirements.txt

py-test:
	cd python-pytest && pytest -ra

py-smoke:
	cd python-pytest && pytest -m smoke

# ---- javascript-jest ------------------------------------------------------
js-install:
	cd javascript-jest && npm install

js-test:
	cd javascript-jest && npm test

js-smoke:
	cd javascript-jest && npm run test:smoke

# ---- java-rest-assured ----------------------------------------------------
java-test:
	cd java-rest-assured && mvn -B test

java-smoke:
	cd java-rest-assured && mvn -B test -Psmoke

# ---- postman / newman -----------------------------------------------------
newman:
	command -v newman >/dev/null 2>&1 || npm install -g newman
	cd postman && ./run-newman.sh dev

# ---- contract-testing-pact ------------------------------------------------
# Consumer generates the pact, provider verifies it — same order as CI.
pact:
	cd contract-testing-pact/consumer/javascript && npm install && npm run test:pact
	cd contract-testing-pact/provider/python && pip install -r requirements.txt && pytest -ra

# ---- housekeeping ---------------------------------------------------------
clean:
	find . -name '__pycache__' -type d -prune -exec rm -rf {} +
	find . -name '.pytest_cache' -type d -prune -exec rm -rf {} +
	rm -rf java-rest-assured/target
	rm -rf postman/reports
	rm -rf javascript-jest/node_modules contract-testing-pact/consumer/javascript/node_modules
