from app.models import db 

class Wallet(db.Model):
    __tablename__ = 'dairy_wallet'

    wallet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dairy_id = db.Column(db.String(length=10), db.ForeignKey('dairy_owner.dairy_id'))
    current_balance = db.Column(db.Numeric)
