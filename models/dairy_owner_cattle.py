from app.models import db
from flask import current_app as app 

class DairyOwnerCattle(db.Model):
    __tablename__ = 'dairy_owner_cattle'

    cattle_id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    dairy_id = db.Column(db.Integer, db.ForeignKey('dairy_owner.dairy_id'))
    
