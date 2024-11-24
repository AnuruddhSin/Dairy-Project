from app.models import db
from flask import current_app as app 

class SupplyTransaction(db.Model):
    __tablename__ = 'supply_transactions'

    # Unique transaction id given to each transaction occurred 
    supply_transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Dairy ID of the dairy who receives the money for the supply if purchased or exchanged for quantity of milk
    dairy_id = db.Column(db.Integer, db.ForeignKey('dairy_owner.dairy_id'))

    # Amount of money which is paid
    amount = db.Column(db.Numeric)

    transaction_date = db.Column(db.Date)

    quantity = db.Column(db.Numeric)

    # Farmer id of the farmer who pays the money
    farmer_id = db.Column(db.String, db.ForeignKey('farmers.farmer_id'))

    # Supply id of the supply which the farmer purchases
    supply_id = db.Column(db.Integer, db.ForeignKey('supplies.supply_id'))

    # String representation of the model
    def __repr__(self) -> str:
        return super().__repr__()
    
    # Function to convert the data in the model to dictionary for ease of use during rendering the data in frontend
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    