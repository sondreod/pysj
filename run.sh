source $(pwd)/venv/bin/activate
$(pwd)/venv/bin/python $(pwd)/pysj/server.py &
$(pwd)/venv/bin/python $(pwd)/pysj/client.py &