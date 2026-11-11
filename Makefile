PY ?= python
.PHONY: data stamp site serve clean
data:   ; $(PY) scripts/run_experiment.py
stamp:  ; $(PY) scripts/stamp.py
site: data stamp ; $(PY) -m mkdocs build --strict
serve: data stamp ; $(PY) -m mkdocs serve
clean:  ; rm -rf site docs/generated .cache
