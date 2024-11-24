from app.models import db

class Product(db.Model):
    __tablename__ = 'product'
    
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    product_no = db.Column(db.Integer)

    product_name = db.Column(db.String(length=255))

    product_description = db.Column(db.String(length=255))

    product_price = db.Column(db.Numeric)

    quantity = db.Column(db.Integer)

    image_url = db.Column(db.String(length=255))

    dairy_id = db.Column(db.String(length=10), db.ForeignKey('dairy_owner.dairy_id'))

    percent_discount = db.Column(db.Numeric)

    available_till = db.Column(db.Date)
    # relation
    supply_transaction_rel = db.relationship('SupplyTransaction', backref='product', lazy=True)
    cart_relation = db.relationship('Cart', backref='product', lazy=True)

    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}