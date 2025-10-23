import os
import peewee
from urllib.parse import urlparse

# Optionally load a .env file if python-dotenv is installed (no hard dependency)
try:
    import importlib

    dotenv = importlib.import_module('dotenv')
    if hasattr(dotenv, 'load_dotenv'):
        dotenv.load_dotenv()
except Exception:
    # python-dotenv not installed or failed to load; ignore and rely on environment
    pass


def _get_db_config():
    # Prefer a DATABASE_URL if provided (format: postgresql://user:pass@host:port/dbname)
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        parsed = urlparse(database_url)
        return {
            'database': parsed.path.lstrip('/'),
            'user': parsed.username,
            'password': parsed.password,
            'host': parsed.hostname or 'localhost',
            'port': int(parsed.port) if parsed.port else 5432,
        }

    # Fall back to individual env vars with sane defaults
    return {
        'database': os.environ.get('POSTGRES_DB', 'database_name'),
        'user': os.environ.get('POSTGRES_USER', 'user'),
        'password': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'host': os.environ.get('POSTGRES_HOST', 'localhost'),
        'port': int(os.environ.get('POSTGRES_PORT', 5432)),
    }


_cfg = _get_db_config()

# Create the Peewee database instance using values from the environment
db = peewee.PostgresqlDatabase(
    _cfg['database'],
    user=_cfg['user'],
    password=_cfg['password'],
    host=_cfg['host'],
    port=_cfg['port'],
)

def initialize_db():
    """Initialize the database connection and create tables if they don't exist."""
    # Import Item lazily here to avoid circular imports where models.item
    # imports `db` from this module at import time.
    from models.item import Item

    db.connect()
    db.create_tables([Item], safe=True)