from flask import Blueprint, jsonify
import peewee

from lib.postdb import db

health_bp = Blueprint('health', __name__, url_prefix='/api/v1')


@health_bp.route('/health', methods=['GET'])
def health_check():
    # Check for database connectivity
    try:
        if db.is_closed():
            db.connect()
        db.execute_sql('SELECT 1')
        if not db.is_closed():
            db.close()
        return jsonify({'status': 'ok'}), 200
    except peewee.OperationalError as e:
        return jsonify({'status': 'error', 'message': f'Database connection failed: {e}'}), 500