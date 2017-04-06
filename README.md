### Simple Flask Json Store

This is strictly meant for development purposes. The application will reset it's
database upon restart.
Running the run-script directly on a python interpreter will prepopulate the datastore with sample data.

#### Dependencies:
* python (>=3.4)
* python-virtualenv
* pip
* postgresql

#### Deployment:
```lang=shell
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
# For production, use:
$ gunicorn --bind 0.0.0.0:5000 run:app
# For development/testing use:
$ python3 ./run.py
```
