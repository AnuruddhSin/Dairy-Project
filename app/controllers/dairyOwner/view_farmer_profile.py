from flask import Blueprint, flash, render_template, redirect, url_for, session
from app.models import db, Farmer, MilkEntry
from sqlalchemy import func
from datetime import timedelta
view_farmer = Blueprint('view_farmer', __name__)

@view_farmer.route('/dairyOwner/view/farmer/<farmer_id>')
def viewFarmer(farmer_id):
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    if farmer_id is None:
        flash("Farmer Id not found please contact support if farmer exists in your dairy list")
        return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))
    
    farmer = Farmer.query.filter_by(farmer_id=farmer_id).first()
    # if farmer.dairy_id != session.get('dairy_id'):
    #     return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))
    milk_entries = MilkEntry.query.filter_by(farmer_id=farmer_id).order_by(MilkEntry.collection_date.desc()).all()

    
    milk_entry_list = [entries.as_dict() for entries in milk_entries]

    return render_template('dairyOwner/FarmerProfile.html', farmer = farmer, milk_entries = milk_entry_list)