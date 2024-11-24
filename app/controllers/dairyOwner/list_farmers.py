from flask import Blueprint, redirect, render_template, session, request, make_response, jsonify, flash, url_for
from app.models import Farmer, DairyOwner, db

list_farmers_bp = Blueprint("list_farmers", __name__)
from sqlalchemy import or_, and_
# Controller Tested and Working Properly

@list_farmers_bp.route("/dairyOwner/Dashboard/milkEntry/farmer/details", methods=["GET" ,"POST"])
def get_all_farmers():
    print(session.get('dairy_id'))
    if request.method=='POST':
        if not session.get('dairy_id'):
            return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
        name = request.form.get('name')
        farmers = Farmer.query.filter(and_(
                Farmer.dairy_id == session.get('dairy_id'),  # Ensure the farmer belongs to the given dairy_id
                or_(Farmer.first_name.ilike(f"%{name}%"))  # Search by name
            )).all()
        farmers_list = [farmer.as_dict() for farmer in farmers]
        
        return render_template('dairyOwner/Dairy_owner_farmers.html', farmers=farmers_list)
    # cannot access if dairy owner is not logged in
    print(session.get('dairy_id'))
    if not session.get('dairy_id'):
        return redirect(url_for("dairy_owner_login_bp.dairyOwnerLogin"))

    # get logged dairy_owner id
    dairy_id = session.get("dairy_id")
    farmers_ = Farmer.query.filter_by(dairy_id=dairy_id).all()
    print(farmers_)

    return render_template('dairyOwner/Dairy_owner_farmers.html', farmers=farmers_)


@list_farmers_bp.route('/dairyOwner/edit/farmer/<farmer_id>', methods=['GET', 'UPDATE'])
def editFarmer(farmer_id):
    if not session.get("dairy_id"):
        return redirect(url_for("dairy_owner_login_bp.DairyOwnerLogin"))
    
    farmer = Farmer.query.get_or_404(farmer_id)

    if request.method == 'POST':
        updated_farmer_id = request.form.get("farmer_id")
        fullname = request.form.get('farmer_name')
        mobile_number = request.form.get('mobile_number')
        email = request.form.get('email')
        state = request.form.get('state')
        district = request.form.get('district')
        taluka = request.form.get('taluka')
        village = request.form.get('village')
        pincode = request.form.get('pincode')

        # Farm info

        farm_name = request.form.get('farm_name')
        address = request.form.get('address')

        # Account Info 

        bank_name = request.form.get('bank_name')
        account_number = request.form.get('account_no')
        branch_name = request.form.get('branch_name')
        ifsc_code = request.form.get('ifsc_code')

        # Dairy Info

        dairy_id = request.form.get('dairy_id')
        preferred_dairy_name = request.form.get("dairy_name")
        dairy_address = request.form.get("dairy_address")
        
        try:
            Farmer.query.filter_by(farmer_id=farmer_id).update({
                "farmer_name" : fullname,
                "farmer_mobile_number" : mobile_number,
                "farmer_email" : email,
                "farmer_state" : state,
                "farmer_district" : district,
                "farmer_taluka" : taluka,
                "farmer_village" : village,
                "farmer_pincode" : pincode,
                "farmer_id" : updated_farmer_id,
                "farm_name" : farm_name,
                "farm_address" : address,
                "farmer_bank_name" : bank_name,
                "farmer_branch_name" : branch_name,
                "farmer_account_no" : account_number,
                "farmer_ifsc_code" : ifsc_code,
                "dairy_id" : dairy_id,
                "preferred_dairy_name" : preferred_dairy_name
            })
            flash("Farmer Added Successfully")
            return redirect(url_for('list_farmer_bp.get_all_farmers'))
        except:
            return redirect(url_for("guest.handle_db_error"))
