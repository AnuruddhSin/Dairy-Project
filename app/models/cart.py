from app.models import db
from sqlalchemy.dialects.postgresql import ARRAY

class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    farmer_id = db.Column(db.String(length=255), db.ForeignKey('farmer.farmer_id'))
    product_name = db.Column(db.String(length=255))
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Numeric)
    is_paid = db.Column(db.Boolean)
    
    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
