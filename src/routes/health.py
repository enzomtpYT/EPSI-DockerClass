from flask import Blueprint, jsonify
import peewee

from lib.postdb import db

health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def health_check():
    # Check for database connectivity
    try:
        db.connect()
        db.close()
    except peewee.OperationalError:
        return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500
    return jsonify({'status': 'ok'}), 200