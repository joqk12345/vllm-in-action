.PHONY: validate build preview clean

validate:
	python3 scripts/validate_kb.py
	npm run check

build:
	npm run build

preview: build
	npm run preview

clean:
	rm -rf dist
