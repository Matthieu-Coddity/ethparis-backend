from server import app, db

class Item(db.Model):
    __tablename__ = 'items'

    hash_item = db.Column(db.String(64), unique=True, index=True,primary_key=True)
    file_name = db.Column(db.String(64), index=True, unique=False)
    price_item = db.Column(db.Integer)
    #file_item=db.Column(db.LargeBinary)

    def __repr__(self):
        return '<hash %r>' % (self.hash_item)