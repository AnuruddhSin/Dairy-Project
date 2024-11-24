from flask import Blueprint, session, redirect, url_for, request, flash

from app.models import DairyOwner, db

update_milk_rate = Blueprint('update_milk_rate', __name__)

@update_milk_rate.route('/dairyOwner/Dashboard/update/today/milk/rate', methods=['PUT'])
def updateMilkRate():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    if request.method == 'PUT':
        today_price = request.form.get('milk_price')
        dairy_owner = DairyOwner.query.filter_by(dairy_id = session.get('dairy_id')).first()

        dairy_owner.milk_price = today_price
        db.session.commit()

        flash("Milk Price Updated successfully")
        return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))