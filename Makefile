#path
DATA_FOLDER := $(CURDIR)/app/data

.PHONY: build
build:
	@docker build \
		-f app/Dockerfile \
		-t pdf-editor-app ./app

.PHONY: run
run:
	@docker run --rm -it \
		--name pdf-editor-app \
		--volume $(DATA_FOLDER):/workspace/data:rw \
		pdf-editor-app

