requirements:
 - python3
 - pip3
 - virtual environments; not really required, but recommended [ https://realpython.com/python-virtual-environments-a-primer/ ]

create/configure virt_env:
 - as an example, my project path is this: dan^melfi@ny4-43:~/Projects/python/Bluefin$
 - python3 -m venv ./venv
 - active environment (accordng to platform guidelines)
 - pip install -r examples/requirements.txt
 - pip install Bluefin-0.0.1-py3-none-any.whl
 - pip install Bluefin-0.0.2-py3-none-any.whl  << the new one

running examples:
 - enable the virtual environment by running the 'source' command in the appropriate directory e.g., source venv/bin/active
 - this is what my command line looks like when I run it
    (venv) dan^melfi@ny4-43:~/Projects/python/Bluefin/examples$ python pub_client_test.py

the sample pubsub client is demonstrating how to subscribe and publish data. This is a *extremely* basic example and there will be more updates to the pubsub client
in the next few days. however, this should be enough to get you started until I can implement a couple more features/requirements.

i have verified this works and connects to a server and an Excel sheet.

Let's have a call sometime tomorrow to discuss future implementation and any confusing/under-documented items.


