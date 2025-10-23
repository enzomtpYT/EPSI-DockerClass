from flask import Blueprint, jsonify
import flask
import peewee

from lib.postdb import db
from models.item import Item
 
items_bp = Blueprint('items', __name__, url_prefix='/api/v1')

@items_bp.route('/items', methods=['GET'])
def get_items():
    try:
        db.connect()
        items = Item.select()
        db.close()
        return jsonify({'status': 'ok', 'data': [item.to_dict() for item in items]}), 200
    except peewee.OperationalError:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

@items_bp.route('/items', methods=['POST'])
def create_item():
    try:
        db.connect()
        data = flask.request.json
        item = Item.create(
            name=data.get('name', 'Sample Item'),
            description=data.get('description', 'This is a sample item.')
        )
        db.close()
    except peewee.OperationalError:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
    return jsonify({'status': 'ok', 'message': 'Item created'}), 201