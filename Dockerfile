FROM debian

RUN apt-get update && apt-get install -y python3 python-pip python-virtualenv gcc python-dev libpq-dev python3-dev

RUN mkdir -p /opt/flask
COPY app /opt/flask/app
COPY requirements.txt /opt/flask
COPY run.py /opt/flask
COPY docker_run.sh /opt/flask
WORKDIR /opt/flask
RUN virtualenv -p /usr/bin/python3 venv
RUN . venv/bin/activate && pip install -r requirements.txt

ENV PG_ADDR=db
ENV PG_PORT=5432

EXPOSE 5000

CMD ["sh","/opt/flask/docker_run.sh"]
#CMD ["sh","/opt/flask/docker_run.sh","DEV"]
