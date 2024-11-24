from app.models import db 

class Payment(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    dairy_id = db.Column(db.String(length=10), db.ForeignKey('dairy_owner.dairy_id'))
    farmer_id = db.Column(db.String, db.ForeignKey('farmer.farmer_id'))
    farmer_name = db.Column(db.String)
    amount = db.Column(db.Numeric)
    method = db.Column(db.String(length=255))

    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}