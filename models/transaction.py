from app.models import db
from flask import current_app as app 

class Transaction(db.Model):

    # Table name in the DB
    __tablename__ = 'transactions'

    # Transaction id of the farmer to whom the amount is paid PRIMARY KEY 
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Wallet id of the farmer
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallet.wallet_id'))

    # Farmer id of the farmer
    farmer_id = db.Column(db.String, db.ForeignKey('farmers.farmer_id'))

    # Dairy id of the dairy owner who pays the farmer
    dairy_id = db.Column(db.Integer, db.ForeignKey('dairy_owner.dairy_id'))

    # The money shown is transaction is borrowed or not
    is_borrowed = db.Column(db.Boolean)

    transaction_date = db.Column(db.Date)

    quantity = db.Column(db.Numeric)
    # Total amount which is transacted
    amount = db.Column(db.Numeric)


    # String representation of the model
    def __repr__(self) -> str:
        return super().__repr__()
    

    # Dict conversion of the data in the model for ease of use during rendering the data in frontend
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}