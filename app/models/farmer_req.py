from app.models import db

class Request(db.Model):
    __tablename__ = 'request'

    req_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmer_id = db.Column(db.String(length=255), db.ForeignKey('farmer.farmer_id'))
    dairy_id = db.Column(db.String(length=10), db.ForeignKey('dairy_owner.dairy_id'))
    farmer_name = db.Column(db.String(length=255))

    
    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}