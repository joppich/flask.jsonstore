import os
from flask import Flask, json
from sqlalchemy_utils import database_exists

def insert_sample_data():
    import requests
    from app.models import Document
    url = 'https://api.github.com/users/moby/repos'
    sample_data = json.loads(requests.get(url).content.decode('utf-8'))
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
        try:
            db.create_all()
        except:
            pass

    from .api import bp as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
