from app.models import db
from flask import current_app as app 

class Wallet(db.Model):
    # Table name of the table
    __tablename__ = 'wallet'

    # Wallet id of the farmer
    wallet_id = db.Column(db.Integer, primary_key = True, autoincrement=True)

    # Total balance available in the wallet of the farmer
    balance = db.Column(db.Numeric)

    # Dairy id of the dairy with which the farmer is associated with
    dairy_id = db.Column(db.Integer, db.ForeignKey('dairy_owner.dairy_id'))

    # Farmer id of the farmer
    farmer_id = db.Column(db.String, db.ForeignKey('farmers.farmer_id'))

    farmer_payment_transactions = db.relationship('Transaction', backref='wallet', lazy=True)

    def __repr__(self) -> str:
        return super().__repr__()