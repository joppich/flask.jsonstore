#!/bin/sh

cd /opt/flask
. venv/bin/activate

if [ "$1" = "DEV" ]
then
	export APP_DEBUG=True
	export APP_DB_URI="postgresql://auric:grandslam@"$PG_ADDR":"$PG_PORT"/dev_db"
	venv/bin/python3 ./run.py
else
	export APP_DEBUG=False
	export APP_DB_URI="postgresql://auric:grandslam@"$PG_ADDR":"$PG_PORT"/prod_db"
	venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 3 run:app --access-logfile - --error-logfile -
fi
