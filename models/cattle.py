from app.models import db 
from flask import current_app as app 

class Cow(db.Model):
    __tablename__   = 'cattle'

    # Unique ID given to cows by the government
    cattle_id = db.Column(db.String(), primary_key=True)

    # Foreign Key farmer_id from Farmers table in the Database 
    # Used to relate every cow with its associated farmer
    farmer_id = db.Column(db.String, db.ForeignKey('farmers.farmer_id'))

    cattle_name = db.Column(db.String())

    breed = db.Column(db.String())

    age = db.Column(db.Integer)

    milk_yield = db.Column(db.Integer)

    health_status = db.Column(db.String())

    # Dont update it using anything triggers and functions are created in psql to update them always
    created_at = db.Column(db.Date)
    updated_at = db.Column(db.Date)


    def __repr__(self) -> str:
        return super().__repr__()

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}