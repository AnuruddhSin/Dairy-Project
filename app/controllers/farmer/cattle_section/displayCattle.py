from flask import Blueprint, session, render_template, redirect, url_for
from app.models import Cow, Farmer


display_cattle = Blueprint('display_cattle', __name__)

@display_cattle.route('/farmer/dashboard/view/cattle')
def showCattles():
    if not session.get('farmer_id'):
        return redirect(url_for('farmer_login_control.farmerLogin'))
    
    cattles = Cow.query.filter_by(farmer_id = session.get('farmer_id')).all()
    farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
    cattle_list = [item.as_dict() for item in cattles]
    print(cattle_list)

    return render_template('farmer/cattle_section/CattleList.html', cattles = cattle_list, farmer = farmer)