from app.models import db
from flask import current_app as app

class Supplies(db.Model):
    __tablename__ = 'supplies'
    # Supply ID of dairy owners INT
    supply_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Supply name VARCHAR(255)
    supply_name = db.Column(db.String(length=255))

    # Price of the supply DECIMAL(5,2)
    price = db.Column(db.Numeric)

    # Dairy id who issues the supplies INT
    dairy_id = db.Column(db.Integer, db.ForeignKey('dairy_owner.dairy_id'))

    # New fields
    # Discount percentage (INT, for e.g., 35 for -35%)
    discount = db.Column(db.Integer)

    # Availability status (BOOLEAN, True if available)
    availability = db.Column(db.Boolean, default=True)

    # Quantity of the supply in stock (INT)
    quantity = db.Column(db.Integer)

    # Description of the supply (VARCHAR(255))
    description = db.Column(db.String(length=255))

    # Image URL (VARCHAR, for product image)
    image_url = db.Column(db.String)

    # Defining Relations with other tables here
    supply_transaction = db.relationship('SupplyTransaction', backref='supplies', lazy=True)

    def repr(self) -> str:
        return super().repr()

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table.columns} 
