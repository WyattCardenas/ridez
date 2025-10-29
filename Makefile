REQUIREMENTS_TXT := $(patsubst %.in,%.txt,$(wildcard requirements/*.in))
PIP_COMPILE := pip-compile --quiet --no-header --allow-unsafe --strip-extras

.PHONY: requirements

# requirements/constraints.txt: requirements/constraints.in
# 	CONSTRAINTS=/dev/null $(PIP_COMPILE) --output-file $@ $^

requirements/%.txt: requirements/%.in
	$(PIP_COMPILE) --output-file $@ $<

reqs: $(REQUIREMENTS_TXT)	## Generate all requirements files

clean-reqs:		## Remove all generated requirements files
	rm -f $(REQUIREMENTS_TXT) requirements/constraints.txt

update-reqs: clean-reqs reqs	## Update all requirements files to latest versions

help:	## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

install-dev: $(REQUIREMENTS_TXT)	## Install development dependencies
	pip install --upgrade pip-tools
	pip-sync $^
