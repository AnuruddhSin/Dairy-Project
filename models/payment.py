from app.models import db 
from flask import current_app as app 

class Payment(db.Model):
    __tablename__ = 'payment'

    payment_id = db.Column(db.Integer(), primary_key=True)
    sale_id = db.Column(db.Integer, nullable=False)
    payment_date = db.Column(db.Date)
    amount_paid = db.Column(db.Numeric)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)

    def __repr__(self) -> str:
        return super().__repr__()