from datetime import datetime
from marshmallow_jsonapi import Schema, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON


db = SQLAlchemy()

class CRUD(object):

    def create(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class Document(db.Model, CRUD):
    __tablename__ = 'documents'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.now())
    doc = db.Column(db.JSON, nullable=False)


class DocumentSchema(Schema):

    id = fields.Integer(dump_only=True)
    created = fields.DateTime(dump_only=True)
    doc = fields.Dict()

    class Meta:
        type_ = 'documents'
        #self_url = '/documents/{id}'
        #self_url_kwargs = {'id': '<id>'}
        strict = True
