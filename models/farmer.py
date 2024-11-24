from datetime import datetime
from sqlalchemy.schema import FetchedValue
from app.models import db
from flask import current_app as app 


# Old Model
class Farmer(db.Model):
    __tablename__ = 'farmers'
    
    # Primary Key in Farmers table used to identify each farmer
    farmer_id = db.Column(db.String(length=10), primary_key=True, autoincrement=False, server_default=FetchedValue())

    # Name of Farmer VARCHAR NOT NULL
    first_name = db.Column(db.String(length=255), nullable=False)

    # Last Name of Farmer VARCHAR NOT NULL
    last_name = db.Column(db.String(length=255), nullable=False)

    # Number of cows the farmer owns
    cows = db.Column(db.Integer)

    # Gender of the farmer (Male/Female)
    gender = db.Column(db.String())

    # Email of farmer NOT NULL VARCHAR
    email = db.Column(db.String(), nullable=False)

    # Mobile Number of Farmer VARCHAR NOT NULL
    phone_number = db.Column(db.String(length=15), nullable=False)

    # Date of Birth of Farmer NOT NULL
    dob = db.Column(db.Date)
    
    # image of farmer
    image_url = db.Column(db.String(), nullable=False)


    # Password for Farmer Login VARCHAR NOT NULL  
    # Password is stored in hashed format using bcrypt
    password = db.Column(db.String(), nullable=False)

    # Farm address VARCHAR 
    address = db.Column(db.String())

    # Timestamp for when the farmer record is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Timestamp for when the farmer record is updated
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key relationship with the dairy_owner table
    dairy_id = db.Column(db.Integer, db.ForeignKey('dairy_owner.dairy_id'))


    # Table relations
    cows_relation = db.relationship('Cow', backref='farmer', lazy=True)
    farmer_bank_relation = db.relationship('FarmerBank', backref='farmer', lazy=True)
    supply_transactions = db.relationship('SupplyTransaction', backref='farmers', lazy=True)
    farmer_payment_transactions_relation = db.relationship('Transaction', backref='farmers', lazy=True)
    milk_entries = db.relationship('MilkEntry', backref='farmers', lazy=True)

    # String representation of Object
    def __repr__(self) -> str:
        return f"<Farmer {self.first_name} {self.last_name}>"
    
    # Converting Object to Dict to render data in frontend
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



# New Model 

# class Farmer(db.Model):
#     __tablename__ = 'farmer'

#     farmer_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    
#     farmer_name = db.Column(db.String(length=255))
    
#     farmer_state = db.Column(db.String(length=255))

#     farmer_dob = db.Column(db.Date)

#     farmer_district = db.Column(db.String(length=255))
    
#     farmer_taluka = db.Column(db.String(length=255))
    
#     farmer_pincode = db.Column(db.Integer)

#     farmer_email = db.Column(db.String(length=255))

#     farmer_cows = db.Column(db.Integer)
    
#     farmer_village = db.Column(db.String(length=255))
    
#     farmer_bank_name = db.Column(db.String(length=255))
    
#     farmer_password = db.Column(db.String(length=255))
    
#     farmer_branch_name = db.Column(db.String(length=255))
    
#     farmer_account_no = db.Column(db.Integer)
    
#     farmer_image_url = db.Column(db.String(length=255))
    
#     farmer_ifsc_code = db.Column(db.String(length=255))
    
#     farmer_mobile_number = db.Column(db.String(length=15))
    
#     total_earnings = db.Column(db.Numeric)
    
#     pending_payment = db.Column(db.Numeric)
    
#     farmer_aadhar_no = db.Column(db.String(length=15))
#     dairy_id = db.Column(db.String(length=255), db.ForeignKey('dairy_owner.dairy_id'))

#     cows_relation = db.relationship('Cow', backref='farmer', lazy=True)
#     milk_transaction_relation = db.relationship('MilkTransaction', backref='farmer', lazy=True)
#     cart_relation = db.relationship('Cart', backref='farmer', lazy=True)
    
#     def __repr__(self) -> str:
#         return super().__repr__()
    
#     def as_dict(self):
#         return {column.name: getattr(self, column.name) for column in self.__table__.columns}