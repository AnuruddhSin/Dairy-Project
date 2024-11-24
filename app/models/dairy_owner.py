from app.models import db 

class DairyOwner(db.Model):
    __tablename__ = 'dairy_owner'
    owner_name = db.Column(db.String(length=255))

    dairy_mobile_number = db.Column(db.String(length=15))

    dairy_id = db.Column(db.String(length=10), primary_key=True, nullable=False)

    total_farmers = db.Column(db.Integer)

    email = db.Column(db.String(length=255))

    dob = db.Column(db.Date)
    
    food_license_no = db.Column(db.String(length=255))
    
    password = db.Column(db.String(length=255))
    
    dairy_name = db.Column(db.String(length=255))
    
    milk_storage_capacity = db.Column(db.Integer)

    # state = db.Column(db.String(length=255))
    
    # district = db.Column(db.String(length=255))
    
    # taluka = db.Column(db.String(length=255))
    
    # village = db.Column(db.String(length=255))

    udyam_aadhar_no = db.Column(db.String(length=255))

    address = db.Column(db.String(length=255))

    bank_name = db.Column(db.String(length=255))
    
    account_no = db.Column(db.String(length=255))
    
    branch_name = db.Column(db.String(length=255))
    
    ifsc_code = db.Column(db.String(length=255))

    pending_payments = db.Column(db.Numeric)

    image_url = db.Column(db.String(length=255))

    wallet_balance = db.Column(db.Numeric)

    total_payments = db.Column(db.Numeric)

    total_revenue = db.Column(db.Numeric)

    milk_price = db.Column(db.Integer)

    # Relations with other tables
    farmer_relation = db.relationship('Farmer', backref='dairy_owner', lazy=True)
    milk_transaction_relation = db.relationship('MilkEntry', backref='dairy_owner', lazy=True)
    dairy_request_relation = db.relationship('Request', backref='dairy_owner', lazy=True)
    wallet_relation = db.relationship('Wallet', backref='dairy_owner', lazy=True)

    @staticmethod
    def generate_dairy_id():
        last_dairy = db.session.query(DairyOwner).order_by(DairyOwner.dairy_id.desc()).first()
        if last_dairy:
            last_id = int(last_dairy.dairy_id[3:])  # Extract numeric part and convert to int
            new_id = last_id + 1
        else:
            new_id = 1  # Start from 1 if no entries exist
        return f"OWN{str(new_id).zfill(4)}"  # Format new_id with leading zeros

    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}