import flask

from routes import items_bp, health_bp
from lib.postdb import initialize_db, db
from models.item import Item
import peewee

app = flask.Flask(__name__)

# Register blueprints
app.register_blueprint(items_bp)
app.register_blueprint(health_bp)

@app.route('/', methods=['GET'])
def root():
    """Root route — returns an HTML page listing all items."""
    try:
        if db.is_closed():
            db.connect()
        items = Item.select()
        items_list = [item.to_dict() for item in items]
        if not db.is_closed():
            db.close()
    except peewee.OperationalError:
        items_list = []
    
    return flask.render_template('items_list.html', items=items_list)

if __name__ == '__main__':
    initialize_db()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)