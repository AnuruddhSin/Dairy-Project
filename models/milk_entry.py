from app.models import db
from flask import current_app as app 

class MilkEntry(db.Model):

    __tablename__ = 'milk_entries'
   
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmer_id = db.Column(db.String, db.ForeignKey('farmers.farmer_id'), nullable=False)
    dairy_id = db.Column(db.Integer, db.ForeignKey('dairy_owner.dairy_id'))
    collection_date = db.Column(db.Date, nullable=False)
    collection_time = db.Column(db.Time, nullable=False)
    quantity_milk = db.Column(db.Float, nullable=False)
    milk_type = db.Column(db.String(50), nullable=False)
    fat_content = db.Column(db.Float, nullable=False)
    snf_content = db.Column(db.Float, nullable=False)
    rate_per_l = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    collected_by = db.Column(db.String(100), nullable=False)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
