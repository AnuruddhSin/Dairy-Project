from app.models import db 

class Farmer(db.Model):
    __tablename__ = 'farmer'

    farmer_id = db.Column(db.String, primary_key=True, autoincrement=False)
    
    farmer_name = db.Column(db.String(length=255))
    
    farmer_state = db.Column(db.String(length=255))

    farmer_dob = db.Column(db.Date)

    farmer_district = db.Column(db.String(length=255))
    
    farmer_taluka = db.Column(db.String(length=255))
    
    farmer_pincode = db.Column(db.Integer)

    farmer_email = db.Column(db.String(length=255))

    farm_name = db.Column(db.String(length=255))
    
    farm_address = db.Column(db.String(length=255))

    farmer_cows = db.Column(db.Integer)
    
    farmer_village = db.Column(db.String(length=255))
    
    farmer_bank_name = db.Column(db.String(length=255))
    
    farmer_password = db.Column(db.String(length=255))
    
    farmer_branch_name = db.Column(db.String(length=255))
    
    farmer_account_no = db.Column(db.Integer)
    
    farmer_image_url = db.Column(db.String(length=255))
    
    farmer_ifsc_code = db.Column(db.String(length=255))
    
    farmer_mobile_number = db.Column(db.String(length=15))
    
    total_earnings = db.Column(db.Numeric)

    withdrawal_method = db.Column(db.String(length=255))
    
    pending_payments = db.Column(db.Numeric)
    
    farmer_aadhar_no = db.Column(db.String(length=15))
    
    dairy_id = db.Column(db.String(length=255), db.ForeignKey('dairy_owner.dairy_id'))
    
    preferred_dairy_name = db.Column(db.String(length=255))
    
    created_at = db.Column(db.Date)

    updated_at = db.Column(db.Date)

    # dairy_address = db.Column(db.String(length=255))
    cows_relation = db.relationship('Cow', backref='farmer', lazy=True)
    milk_transaction_relation = db.relationship('MilkEntry', backref='farmer', lazy=True)
    cart_relation = db.relationship('Cart', backref='farmer', lazy=True)
    farmer_request_relation = db.relationship('Request', backref='farmer', lazy=True)
    
    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}