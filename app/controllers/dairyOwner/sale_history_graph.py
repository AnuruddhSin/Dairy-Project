from flask import Blueprint, session, redirect, url_for, jsonify
from app.models import SupplyTransaction, db
from sqlalchemy import extract, func

sales_history = Blueprint('sales_history', __name__)

month_map = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}


@sales_history.route('/get_bar_heights')
def get_bar_heights():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    monthly_summary_query = (
        db.session.query(
            extract('month', SupplyTransaction.transaction_date).label('month'),
            func.sum(SupplyTransaction.amount).label('total_amount')
        )
        .group_by(extract('month', SupplyTransaction.transaction_date))
        .order_by(extract('month', SupplyTransaction.transaction_date))
        .all()
    )

    max_amount = max((float(total_amount or 0) for _, total_amount in monthly_summary_query), default=1)

    # Convert the query result into a dictionary with month abbreviations and calculate percentages
    bar_heights = {
        month_map[int(month)]: (float(total_amount or 0) / max_amount) * 100
        for month, total_amount in monthly_summary_query
    }
    print(bar_heights)
    return jsonify(bar_heights)

@sales_history.route('/each_product_graph/<product_id>')
def each_product_graph_height(product_id):
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    monthly_summary_query = (
        db.session.query(
            extract('month', SupplyTransaction.transaction_date).label('month'),
            func.sum(SupplyTransaction.amount).label('total_amount')
        )
        .filter(SupplyTransaction.supply_id == product_id)
        .group_by(extract('month', SupplyTransaction.transaction_date))
        .order_by(extract('month', SupplyTransaction.transaction_date))
        .all()
    )

    max_amount = max((float(total_amount or 0) for _, total_amount in monthly_summary_query), default=1)

    
    bar_heights = {
        month_map[int(month)]: (float(total_amount or 0) / max_amount) * 100
        for month, total_amount in monthly_summary_query
    }
    print(bar_heights)
    return jsonify(bar_heights)