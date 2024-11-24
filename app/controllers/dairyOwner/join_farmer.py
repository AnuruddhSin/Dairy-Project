from flask import Blueprint, flash, redirect, url_for, render_template, request, session
from app.models import db, Farmer, Request, DairyOwner, PastFarmer

join_new_farmer = Blueprint('join_new_farmer', __name__)

@join_new_farmer.route('/dairyOwner/add/new/farmer', methods=['GET','POST'])
def joinFarmer():
    if session.get('dairy_id') is None:
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    


    if request.method == 'POST':
        print(request.form)
        farmer_uid = request.form.get("farmer_uid")
        print(farmer_uid)
        dairy_owner = DairyOwner.query.filter_by(dairy_id = session.get('dairy_id')).first()
        farmer = Farmer.query.filter_by(farmer_id=farmer_uid).first()
        if not farmer:
            flash("Farmer id not found. Please enter valid farmer id")
            return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))
        past_farmer = PastFarmer.query.filter_by(farmer_id = farmer_uid).first()
        if past_farmer:
            db.session.delete(past_farmer)

        if farmer is None:
            flash("Invalid Farmer ID please enter a valid farmer ID")
            return redirect(url_for('join_new_farmer.joinFarmer'))
        
        # if farmer.dairy_id is None:
        dairy_id = session.get('dairy_id')
        farmer.dairy_id = dairy_id
        dairy_owner.total_farmers += 1
        db.session.commit()
        flash("Farmer Added Successfully to Dairy")
        return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))
        
        # else:
        #     new_request = Request(
        #         farmer_id = farmer_uid,
        #         dairy_id = session.get('dairy_id'),
        #     )

            # db.session.add(new_request)
            # db.session.commit()
            # # Send mail or SMS notification
            # from Dairyproject.app import mail
            
            # # Send notification to farmer for dairy acception
            # flash("Farmer is working for another dairy Notification sent successfully wait for the farmer to accept it")
            # return redirect(url_for('join_new_farmer.joinFarmer'))
        
    # return render_template('dairyOwner/Dashboard/JoinFarmer.html')