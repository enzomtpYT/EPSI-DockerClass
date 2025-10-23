from flask import Blueprint, jsonify
import peewee

from lib.postdb import db
from models.item import Item
 
items_bp = Blueprint('items', __name__)

@items_bp.route('/items', methods=['GET'])
def get_items():
    # Fetch items from the database
    try:
        db.connect()
        items = Item.select()
        db.close()
        return jsonify({'status': 'ok', 'data': [item.to_dict() for item in items]}), 200
    except peewee.OperationalError:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
