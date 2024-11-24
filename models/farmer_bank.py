from app.models import db
from flask import current_app as app 

class FarmerBank(db.Model):

    # Table name in Database
    __tablename__ = 'farmer_bank'

    # Account Number of farmer VARCHAR
    account_no = db.Column(db.String(), primary_key=True)

    # Bank Name VARCHAR NOT NULL
    bank_name = db.Column(db.String(), nullable=False)

    # Branch Name of Bank VARCHAR NOT NULL
    branch_name = db.Column(db.String(), nullable=False)

    # IFSC Code of the bank
    ifsc_code = db.Column(db.String(), nullable=False)

    # Foreign Key Farmer ID used to associate farmer with his bank details
    farmer_id = db.Column(db.String(length=10), db.ForeignKey('farmers.farmer_id'))


    # String representation of Object
    def __repr__(self) -> str:
        return super().__repr__()
    
    # Converting Object to Dict to render data in frontend
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}