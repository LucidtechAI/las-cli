.PHONY: publish
publish:
	tox -e publish

.PHONY: test
test:
	@echo "Running test suite..."
	tox -e py

.PHONY: prism-start
prism-start:
	@echo "Starting mock API..."
	docker run -t \
		--init \
		--detach \
		-p 4010:4010 \
		stoplight/prism:4.5.0 mock -h 0.0.0.0 \
		https://raw.githubusercontent.com/LucidtechAI/cradl-docs/master/static/oas.json \
		> /tmp/prism.cid


.PHONY: prism-stop
prism-stop:
ifeq ("$(wildcard /tmp/prism.cid)","")
	@echo "Nothing to stop."
else
	docker stop $(CID)
endif

