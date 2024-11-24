from app.models import db


class MilkTransaction(db.Model):
    __tablename__ = 'milk_transactions'
    farmer_name = db.Column(db.String(length=255))
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    farmer_mobile_number = db.Column(db.String(length=255), db.ForeignKey('farmer.farmer_mobile_number'))
    time_added = db.Column(db.Time)
    milk_qty = db.Column(db.Integer)
    fat = db.Column(db.Numeric)
    rate = db.Column(db.Numeric)
    total_amount = db.Column(db.Numeric)
    farmer_id = db.Column(db.Integer, db.ForeignKey('farmer.farmer_id'))
    dairy_id = db.Column(db.String(length=255), db.ForeignKey('dairy_owner.dairy_id'))
    created_at = db.Column(db.Date)

    def __repr__(self) -> str:
        return super().__repr__()

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
