# Icarus
async queue worker for openfaas
![alt text](http://nxcache.nexon.net/umbraco/8218/calypso.jpg)
## Usage:
- make build-local
- make deploy-local
- virtualenv venv
- source venv/bin/activate
- pip install -r ./requirements.txt
- export PYTHONPATH=$PYTHONPATH:.
- python ./demos/demo_callback_url.py
- python ./demos/demo_async_result.py
