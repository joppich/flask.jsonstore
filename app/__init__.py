import os
from flask import Flask, json

def insert_sample_data():
    import certifi
    import urllib3
    from app.models import Document
    url = 'https://api.github.com/users/MaibornWolff/repos'
    http_ext = urllib3.PoolManager(
    # set a useragent to comply with the github api
        headers={"user-agent" : \
                 "Mozilla/5.0 (Windows NT 6.3; rv:36.0)\
                 Gecko/20100101 Firefox/36.0"},
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where()
    )
    sample_data = json.loads(http_ext.request('GET', url).data.decode('utf-8'))
    for x in sample_data:
        d = Document(doc=x)
        d.create(d)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('APP_DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.environ.get('APP_DEBUG', False)

    from app.models import db
    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()


    from .api import bp as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
