from flask import Blueprint, redirect, render_template, url_for, session, request
from app.models import db, Farmer, MilkEntry
from datetime import datetime
farmer_dashboard_bp = Blueprint('farmer_dashboard_bp', __name__)

@farmer_dashboard_bp.route('/farmer/Dashboard')
def farmerDashboard():
    if not session.get('farmer_id'):
        return redirect(url_for('farmer_login_control.farmerLogin'))

    farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
    print(farmer.farmer_account_no)
    account_no_str = str(farmer.farmer_account_no)
    if len(account_no_str) <= 8:
        hidden_account_no = account_no_str[0] + "*" * (len(account_no_str) - 2) + account_no_str[-1]
    else:
        hidden_account_no = account_no_str[:5] + "*" * (len(account_no_str) - 8) + account_no_str[-3:]
    current_date = datetime.now().date()
    milk_entries = MilkEntry.query.filter_by(farmer_id = session.get('farmer_id')).all()
    entry_list = [item.as_dict() for item in milk_entries]
    print(entry_list)
    return render_template("farmer/Dashboard/FarmerDashboard.html", farmer = farmer.as_dict(), account_no = hidden_account_no, current_date = current_date, milk_entry = entry_list, farmer_image_url=farmer.farmer_image_url)