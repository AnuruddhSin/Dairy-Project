from app.models import db

class Delivery(db.Model):
    __tablename__ = 'delivery_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmer_id = db.Column(db.String(length=255), db.ForeignKey('farmer.farmer_id'))
    dairy_id = db.Column(db.String(length=10), db.ForeignKey('dairy_owner.dairy_id'))
    name = db.Column(db.String(length=255))
    mobile_no = db.Column(db.String(length=255))
    alternate_mobile_number = db.Column(db.String(length=255))
    state = db.Column(db.String(length=255))
    district = db.Column(db.String(length=255))
    taluka = db.Column(db.String(length=255))
    village = db.Column(db.String(length=255))
    pincode = db.Column(db.Integer)
    nearby_landmark = db.Column(db.String(length=255))

    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}