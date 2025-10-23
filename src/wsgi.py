"""
WSGI entry point for the Flask application.
This module initializes the database and exposes the Flask app for WSGI servers.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from index import app
from lib.postdb import initialize_db

initialize_db()

if __name__ == "__main__":
    # For development only - use gunicorn in production
    app.run(host='0.0.0.0', port=5000, debug=True)
