import peewee

from lib.postdb import db

class Item(peewee.Model):
    """Peewee model for items.

    Fields:
    - id: Auto-incrementing primary key.
    - name: Name of the item (string).
    - description: Description of the item (string).
    """
    id = peewee.AutoField()
    name = peewee.CharField(max_length=50)
    description = peewee.TextField()

    class Meta:
        database = db
        table_name = 'items'
    
