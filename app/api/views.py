from flask import request, jsonify, url_for, redirect
from app.models import db
from app.models import Document, DocumentSchema
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from . import bp

schema = DocumentSchema()

@bp.errorhandler(404)
def not_found(error):
    response = jsonify({'code': 404,'message':'Not found'})
    return response, 404


@bp.route('/')
def index():
    return redirect(url_for('static',filename='index.html'))


@bp.route('/documents')
def get_list():
    doc_query = Document.query.all()
    results = schema.dump(doc_query, many=True).data
    return jsonify(results), 200


@bp.route('/documents/<int:id>')
def get(id):
    doc_query = Document.query.get_or_404(id)
    result = schema.dump(doc_query).data
    return jsonify(result), 200


@bp.route('/documents/create', methods=['GET','POST'])
def post():
    raw_dict = request.get_json(force=True)
    try:
        schema.validate(raw_dict)
        doc_dict = raw_dict['data']['attributes']
        doc = Document(doc=doc_dict['doc'])
        doc.create(doc)
        query = Document.query.get(doc.id)
        result = schema.dump(query).data
        return jsonify(result), 201
    except ValidationError as ve:
        response = jsonify({'code': 403,'message': ve.messages})
        return response, 403
    except SQLAlchemyError as e:
        db.session.rollback()
        resp = jsonify({'code': 500,'message': str(e)})
        return response, 500


@bp.route('/documents/update/<int:id>', methods=['GET','POST'])
def patch(id):
    raw_dict = request.get_json(force=True)
    try:
        schema.validate(raw_dict)
        doc_dict = raw_dict['data']['attributes']
        doc = Document.query.get_or_404(id)
        setattr(doc,'doc',doc_dict['doc'])
        doc.update()
        query = Document.query.get(doc.id)
        result = schema.dump(query).data
        return jsonify(result), 200
    except ValidationError as ve:
        response = jsonify({'code': 403,'message': ve.messages})
        return response, 403
    except SQLAlchemyError as e:
        db.session.rollback()
        response = jsonify({'code':500,'message':str(e)})
        return response, 500


@bp.route('/documents/delete/<int:id>')
def delete(id):
    document = Document.query.get_or_404(id)
    try:
        document.delete(document)
        response = jsonify({'message': 'deleted'})
        return response, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        response = jsonify({'code': 500, 'message': str(e)})
        return response, 500
