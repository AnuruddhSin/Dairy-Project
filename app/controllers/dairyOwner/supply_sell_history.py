from flask import Blueprint, redirect, render_template, session, request, make_response, jsonify, flash, url_for
from app.models import Farmer, DairyOwner, SupplyTransaction, Product, db

supply_sell_history_bp = Blueprint("supply_sell_history", __name__)

@supply_sell_history_bp.route("/sell_history", methods=["GET", "POST"])
def sell_history():
    # if dairy owner is not logged in, redirect to login screen
    if not session.get('dairy_id'):
        return redirect(url_for("dairy_owner_login_bp.dairyOwnerLogin"))
    
    dairy_id = session.get('dairy_id')

    dairy_owner = DairyOwner.query.filter_by(dairy_id=dairy_id).first()

    sell_data = []

    if dairy_owner:
        supply_transactions = dairy_owner.supply_transactions

        for transaction in supply_transactions:
            sell_data.append({
            "customer_name": db.session.query(Farmer.first_name).filter_by(farmer_id=transaction.farmer_id).scalar(),
            "order_Id": transaction.supply_transaction_id,
            "date": transaction.transaction_date,
            "quantity": transaction.quantity,
            "amount": transaction.amount,
            "product_name": db.session.query(Product.product_name).filter_by(product_id=transaction.supply_id).scalar(),
            "product_img": db.session.query(Product.image_url).filter_by(product_id=transaction.supply_id).scalar() 
            })

        return render_template("dairyOwner/supply_sell_history.html", sell_data=sell_data)
