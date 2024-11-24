from flask import Blueprint, session, redirect, render_template, url_for, request, jsonify, flash
from app.models import Farmer, db, Request
import bcrypt
from datetime import datetime

farmer_validate = Blueprint('farmer_validate', __name__)

# Route used for validation of OTP sent to user
@farmer_validate.route("/farmer/validate-otp", methods=["GET", "POST"])
def validate_otp():
    if request.method == "POST":
        # Fetching Data from frontend
        email_otp = request.form.get("email_otp")
        mobile_otp = request.form.get('mobile_otp')

        current_date = datetime.now().date()
        # Validating OTP
        # Else it will return 404 NOT FOUND
        if int(email_otp) == int(session.get('email_otp')) and int(mobile_otp) == int(session.get('mobile_otp')):
            farmer_data = session.get('farmer_data')
            # photo_url = session.get('photo_url')  # Fetch profile image URL from session 

            # Creating new Farmer Model to insert in Database
            new_farmer = Farmer(
                farmer_id = farmer_data['farmer_id'],
                farmer_name = farmer_data['farmer_name'],
                farmer_district = farmer_data['district'],
                farmer_taluka = farmer_data['taluka'],
                farmer_pincode = farmer_data['pincode'],
                farmer_village = farmer_data['village'],
                farmer_state = farmer_data['state'],
                farmer_mobile_number=farmer_data["mobile_number"],
                farmer_email=session['email'],
                farmer_aadhar_no = farmer_data['aadhar_no'],
                total_earnings = 0,
                pending_payments = 0,
                farmer_bank_name = farmer_data['bank_name'],
                farmer_branch_name = farmer_data['branch_name'],
                farmer_account_no = farmer_data['account_no'],
                farmer_ifsc_code = farmer_data['ifsc_code'],
                farmer_dob=farmer_data["dob"],
                farmer_password = bcrypt.hashpw(farmer_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                farmer_image_url=farmer_data.get("photo_url"),
                farmer_cows = 0,
                farm_name = farmer_data['farm_name'],
                farm_address = farmer_data['farm_address'],
                created_at = current_date,
                updated_at = current_date
            )
            
            print("Added farmer request to dairy")
            print("Photo URL:", new_farmer.farmer_image_url) #debug
            
            db.session.add(new_farmer)
            
            # This commit is done to get farmer id which are foreign keys in farmer bank and cows table
            db.session.commit()
            new_farmer_request = Request(
                farmer_id = farmer_data['farmer_id'],
                dairy_id = session.get('dairy_id')
            )
            db.session.add(new_farmer_request)
            db.session.commit()
            # Clearing session data
            session.pop('otp', None)
            session.pop('email', None)
            session.pop('photo_url', None)  # Clear profile image URL from session
            
            farmer = Farmer.query.filter_by(farmer_email=farmer_data['email']).first()
            farmer_dict = farmer.as_dict()
            session['farmer_id'] = farmer_dict['farmer_id']
            session.pop('farmer_data', None)
            return jsonify({'success': True, 'message': "OTP verified"}), 200
        else:
            return jsonify({'success': False, 'message': "Invalid OTP"}), 400


@farmer_validate.route('/RegistrationSuccessfull')
def success_page():
    farmer_id = session.get('farmer_id')
    flash("Successful Registration!", 'success')
    return render_template('farmer/success.html', farmer_id=farmer_id)