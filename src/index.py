import flask

from routes import items_bp, health_bp
from lib.postdb import initialize_db

app = flask.Flask(__name__)

# Register blueprints
app.register_blueprint(items_bp)
app.register_blueprint(health_bp)

@app.route('/', methods=['GET'])
def root():
    """Empty root route — returns 200 with empty body."""
    return '', 200

if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)