test: tests/*.py
	@python3 -m unittest tests/config.py tests/http_server.py tests/velox.py tests/utils.py
