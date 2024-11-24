from app.models import db 

class Cow(db.Model):
    __tablename__ = 'cow'

    animal_id = db.Column(db.String(length=255), primary_key=True, autoincrement=False)

    farmer_name = db.Column(db.String(length=255))
    farmer_id = db.Column(db.String, db.ForeignKey('farmer.farmer_id'))
    state = db.Column(db.String(length=255))
    district = db.Column(db.String(length=255))
    taluka = db.Column(db.String(length=255))
    village = db.Column(db.String(length=255))
    animal_type = db.Column(db.String(length=255))
    cow_type = db.Column(db.String(length=255))
    gender = db.Column(db.String(length=255))
    is_milking = db.Column(db.Boolean)
    uploaded_on = db.Column(db.Date)
    online_verified = db.Column(db.Boolean)
    online_remark = db.Column(db.String(length=255))
    

    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}