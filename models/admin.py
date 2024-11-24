from app.models import db 
from flask import current_app as app 

class Admin(db.Model):
    __tablename__ = "admin"

    admin_id = db.Column(db.Integer, primary_key = True)
    photo_url = db.Column(db.String)
    username = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)

    def __repr__(self) -> str:
        return super().__repr__()
    
    