from app.models import db 
from flask import current_app as app 

class DairyOwner(db.Model):

    # Dairy ID unique ID given to each dairy owner INT AUTO INCREMENT PRIMARY KEY
    dairy_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    owner_name = db.Column(db.String(length=255))
    # Email of the dairy owner VARCHAR(255)
    email = db.Column(db.String(length=255))

    # Password for dairy owner to login VARCHAR(255) 
    # The password is stored in hashed format
    password = db.Column(db.String(length=255))

    storage_capacity = db.Column(db.Integer())

    # Address of the dairy VARCHAR(255)
    address = db.Column(db.String(length=255))

    # Phone number of dairy owner VARCHAR(15) 
    phone_number = db.Column(db.String(length=10))

    bank_name = db.Column(db.String(length=255))

    account_no = db.Column(db.Integer)

    branch_name = db.Column(db.String(length=255))

    ifsc_code = db.Column(db.String(length=255))
    
    photo_url = db.Column(db.String())

    # Date of Birth of DairyOwner
    dob = db.Column(db.Date)

    # Defining Relations with other tables here
    supplies = db.relationship('Supplies', backref='dairy_owner', lazy=True)
    farmer_transactions = db.relationship('Transaction', backref='dairy_owner', lazy=True)
    supply_transactions = db.relationship('SupplyTransaction', backref='dairy_owner', lazy=True)
    farmers = db.relationship('Farmer', backref='dairy_owner', lazy=True)
    dairy_owner_cattle = db.relationship('DairyOwnerCattle', backref='dairy_owner', lazy=True)
    milk_entry = db.relationship('MilkEntry', backref='dairy_owner', lazy=True)
    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



# New Model

# class DairyOwner(db.Model):
#     __tablename__ = 'dairy_owner'
#     owner_name = db.Column(db.String(length=255))
#     dairy_id = db.Column(db.String(length=10), primary_key=True)
#     email = db.Column(db.String(length=255))
#     dob = db.Column(db.Date)
#     food_license_no = db.Column(db.String(length=255))
#     password = db.Column(db.String(length=255))
#     dairy_name = db.Column(db.String(length=255))
#     milk_storage_capacity = db.Column(db.Integer)

#     state = db.Column(db.String(length=255))
#     district = db.Column(db.String(length=255))
#     taluka = db.Column(db.String(length=255))
#     village = db.Column(db.String(length=255))

#     bank_name = db.Column(db.String(length=255))
#     account_no = db.Column(db.String(length=255))
#     branch_name = db.Column(db.String(length=255))
#     ifsc_code = db.Column(db.String(length=255))

#     pending_payments = db.Column(db.Numeric)

#     farmer_relation = db.relationship('Farmer', backref='dairy_owner', lazy=True)
#     milk_transaction_relation = db.relationship('MilkTransaction', backref='dairy_owner', lazy=True)
    

#     def __repr__(self) -> str:
#         return super().__repr__()
    
#     def as_dict(self):
#         return {column.name: getattr(self, column.name) for column in self.__table__.columns}