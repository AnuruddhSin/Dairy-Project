from flask import Blueprint, render_template, session, url_for, redirect, request, flash
from app.models import db, Farmer
from datetime import datetime
import bcrypt

validate_farmer_to_dairy_bp = Blueprint('validate_farmer_to_dairy_bp', __name__)

# Testing Complete
@validate_farmer_to_dairy_bp.route('/dairyOwner/validate/farmer', methods=['GET', 'POST'])
def ValidateFarmerToDairy():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    if request.method == 'POST':
        current_date = datetime.now().date()
        email_otp = request.form.get('email_otp')
        mobile_otp = request.form.get('mobile_otp')
        if int(email_otp) == int(session.get('email_otp')) and int(mobile_otp) == int(session.get('mobile_otp')):
            farmer_data = session.get('farmer_data')
            password = "abcd"
            new_farmer = Farmer(
                farmer_id = 132153253431,
                farmer_name = farmer_data['farmer_name'],
                farmer_mobile_number=farmer_data['mobile_number'],
                farmer_email=session['email'],
                dairy_id=farmer_data['dairy_id'],
                farmer_dob=farmer_data['dob'],
                farmer_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                # address=farmer_data['address'],
                farmer_state = farmer_data['state'],
                farmer_aadhar_no = farmer_data['aadhar_no'],
                farmer_district = farmer_data['district'],
                farmer_taluka = farmer_data['taluka'],
                farmer_pincode = farmer_data['pincode'],
                farmer_village = farmer_data['village'],
                farmer_image_url="res.saash9fnoia.com",  # Save the image URL in the Farmer model
                farmer_account_no=farmer_data['account_no'],
                farmer_bank_name=farmer_data['bank_name'],
                farmer_branch_name=farmer_data['branch_name'],
                farmer_ifsc_code=farmer_data['ifsc_code'],
                created_at = current_date,
                updated_at = current_date
            )
            db.session.add(new_farmer)

            
            
            db.session.commit()
            
            flash("Farmer registered successfully!")
            return redirect(url_for('dairy_owner_dashboard_bp.DairyDashboard'))
        else:
            flash("Invalid OTPs. Please try again.")
            return redirect(url_for('validate_farmer_to_dairy_bp.ValidateFarmerToDairy'))
    
    return render_template('dairyOwner/validateFarmerToDairy.html')