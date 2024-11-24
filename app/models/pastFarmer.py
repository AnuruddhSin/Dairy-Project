from app.models import db

class PastFarmer(db.Model):
    __tablename__ = "past_farmer"
    farmer_id = db.Column(db.String(length=255), primary_key = True)
    dairy_id = db.Column(db.String(length=10))
    location = db.Column(db.String(length=255))
    phone_no = db.Column(db.String(length=15))
    farmer_name = db.Column(db.String(length=255))
    farmer_image_url = db.Column(db.String(length=255))
    
    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}