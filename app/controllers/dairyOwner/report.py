import csv
from flask import Blueprint, render_template, redirect, url_for, session, Response
from app.models import MilkEntry, Payment, db , DairyOwner

dairy_report = Blueprint("dairy_report", __name__)

@dairy_report.route('/dairyOwner/report')
def view_reports():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))
    dairyOwner = DairyOwner.query.filter_by(dairy_id = session.get('dairy_id')).first()
    return render_template('dairyOwner/Report.html', dairy_owner = dairyOwner)

@dairy_report.route('/dairyOwner/report/wallet')
def wallet_history():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))

    payments = Payment.query.filter_by(dairy_id=session.get('dairy_id')).all()
    return render_template('dairyOwner/wallet_table.html', payments=payments)

@dairy_report.route('/dairyOwner/report/milk_collection')
def milk_collection_history():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))

    milk_entries = MilkEntry.query.filter_by(dairy_id=session.get('dairy_id')).all()
    return render_template('dairyOwner/milk_collection_table.html', milk_entries=milk_entries)

# @dairy_report.route('/dairyOwner/report/product_sales')
# def product_sales_history():
#     if not session.get('dairy_id'):
#         return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))

#     product_sales = ProductSales.query.filter_by(dairy_id=session.get('dairy_id')).all()
#     return render_template('dairyOwner/product_sell_table.html', product_sales=product_sales)

@dairy_report.route('/dairyOwner/report/milk-collection/download')
def download_milk_collection():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))

    milk_entries = MilkEntry.query.filter_by(dairy_id=session.get('dairy_id')).all()
    
    # Create CSV data
    csv_data = "Entry ID, Farmer ID, Quantity, Fat, Date\n"
    for entry in milk_entries:
        csv_data += f"{entry.entry_id}, {entry.farmer_id}, {entry.quantity}, {entry.fat}, {entry.date}\n"
    
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=milk_collection.csv"}
    )

# @dairy_report.route('/dairyOwner/report/product-sales/download')
# def download_product_sales():
#     if not session.get('dairy_id'):
#         return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))

#     product_sales = ProductSales.query.filter_by(dairy_id=session.get('dairy_id')).all()
    
#     # Create CSV data
#     csv_data = "Sale ID, Product Name, Quantity, Price, Date\n"
#     for sale in product_sales:
#         csv_data += f"{sale.sale_id}, {sale.product_name}, {sale.quantity}, {sale.price}, {sale.date}\n"
    
#     return Response(
#         csv_data,
#         mimetype="text/csv",
#         headers={"Content-disposition": "attachment; filename=product_sales.csv"}
#     )