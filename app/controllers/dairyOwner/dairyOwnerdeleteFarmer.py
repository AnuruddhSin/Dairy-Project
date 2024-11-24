# from flask import Blueprint, redirect, render_template, session, url_for
# from app.models import Farmer, DairyOwner, db, PastFarmer
# delete_farmer = Blueprint("delete_farmer", __name__)


# @delete_farmer.route('/dairyOwner/dashboard/delete/farmer/<farmer_id>')
# def deleteFarmer(farmer_id):
#     if not session.get('dairy_id'):
#         return redirect(url_for("dairy_owner_login_bp.dairyOwnerLogin"))
    
#     farmer = Farmer.query.filter_by(farmer_id=farmer_id).first()
#     past_farmer = PastFarmer(farmer_id = farmer_id, dairy_id = session.get('dairy_id'), location = farmer.farm_address, phone_no = farmer.farmer_mobile_number)
#     db.session.add(past_farmer)
#     farmer.dairy_id = None
#     db.session.commit()

#     return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))

from flask import Blueprint, redirect, render_template, session, url_for, flash
from app.models import Farmer, DairyOwner, db, PastFarmer

delete_farmer = Blueprint("delete_farmer", __name__)

@delete_farmer.route('/dairyOwner/dashboard/delete/farmer/<farmer_id>', methods=['GET', 'POST'])
def deleteFarmer(farmer_id):
    if not session.get('dairy_id'):
        return redirect(url_for("dairy_owner_login_bp.dairyOwnerLogin"))
    
    # Find the farmer in the Farmer table
    farmer = Farmer.query.filter_by(farmer_id=farmer_id).first()
    if not farmer:
        flash("Farmer not found.", "error")
        return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))

    try:
        # Add farmer details to PastFarmer
        past_farmer = PastFarmer(
            farmer_id=farmer_id,
            dairy_id=session.get('dairy_id'),
            location=farmer.farm_address,
            phone_no=farmer.farmer_mobile_number,
            farmer_name = farmer.farmer_name,
            farmer_image_url = farmer.farmer_image_url
        )
        db.session.add(past_farmer)
        dairy_owner = DairyOwner.query.filter_by(dairy_id = session.get('dairy_id')).first()
        dairy_owner.total_farmers -= 1
        # Set the farmer's dairy_id to None, indicating removal from the current dairy
        farmer.dairy_id = None
        db.session.commit()
        flash("Farmer moved to past records successfully.", "success")
        print("Message flashed")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred while deleting the farmer: {e}", "error")
    
    return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))
