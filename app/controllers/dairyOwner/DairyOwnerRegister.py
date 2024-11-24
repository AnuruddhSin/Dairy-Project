# Dairy Owner Bank Details Added

from flask import Blueprint, session, render_template, redirect, url_for, request, flash, jsonify
import bcrypt
from datetime import datetime
from app.models import db
import cloudinary.uploader
from flask_mail import Message
from app.models import DairyOwner
from .generate_otp import GenerateRandomOTP

dairy_owner_register = Blueprint('dairy_owner_register', __name__)

@dairy_owner_register.route('/dairyOwner/register', methods=["GET", "POST"])
def dairyOwnerRegister():
    if request.method == 'POST':
        print("Method executed")
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get("confirm_password")
        food_license_no = request.form.get('food-license')
        dairy_name = request.form.get("dairy-name")
        
        # NOTE: state district taluka village fields are not yet updated in dairy owner registration form
        # state = request.form.get('state')
        # district = request.form.get('district')
        # taluka = request.form.get('taluka')
        # village = request.form.get('village')
        # Check if passwords match
        if password != confirm_password:
            flash("Confirm Password not matching, please enter the same password.")
            return jsonify({'success': False, 'message': "Confirm Password not matching, please enter the same password"}), 400

        dob = request.form.get('dob')
        dob_date = datetime.strptime(dob, '%Y-%m-%d')  # Format: 'YYYY-MM-DD'
        today = datetime.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))

        # Age validation: Must be at least 16 years old
        if age < 16:
            flash("You must be at least 16 years old to register.", "error")
            return jsonify({'success': False, 'message': "You must be at least 16 years old to register."}), 400

        # Retrieve form data
        owner_name = request.form.get('fullname')
        address = request.form.get('address')
        phone_number = request.form.get('mobile_number')
        bank_name = request.form.get('bank_name')
        account_no = request.form.get('account_no')
        branch_name = request.form.get('branch_name')
        ifsc_code = request.form.get('ifsc_code')
        milk_storage_capacity = request.form.get('milk_storage')
        no_of_cattle = int(request.form.get('no_of_cattle'))

        # Collect cattle IDs
        cattle_ids = []
        for i in range(1, no_of_cattle + 1):
            cattle_id = request.form.get(f'cattle_{i}')
            if cattle_id:
                cattle_ids.append(cattle_id)

        # Upload profile image to Cloudinary if provided
        image_url = None
        image = request.files.get("profile_image")
        if image:
            result = cloudinary.uploader.upload(image)
            image_url = result.get('url')

        # Ensure all mandatory fields are filled
        #BASIC INFORMATION
        if not owner_name:
            flash("Please enter the owner's full name.", 'error')
            return jsonify({'success': False, 'message': "Please enter the owner's full name."}), 400
        elif not phone_number:
            flash("Please enter the phone number.", 'error')
            return jsonify({'success': False, 'message': "Please enter the phone number."}), 400
        elif not email:
            flash("Please enter an email address.", 'error')
            return jsonify({'success': False, 'message': "Please enter an email address."}), 400
        elif not dob:
            flash("Please enter the date of birth.", 'error')
            return jsonify({'success': False, 'message': "Please enter the date of birth."}), 400
        elif not food_license_no:
            flash("Please enter the food license number.", 'error')
            return jsonify({'success': False, 'message': "Please enter the food license number."}), 400
        
        # Removed state, taluka, district, village from the form left uncommented if further use needed
        # If use needed add the columns in the database tables they are commented in models

        # elif not village:
        #     flash("Please enter the village name.", 'error')
        #     return jsonify({'success': False, 'message': "Please enter the village name."}), 400
        # elif not district:
        #     flash("Please enter the district name.", 'error')
        #     return jsonify({'success': False, 'message': "Please enter the district name."}), 400
        # elif not taluka:
        #     flash("Please enter the taluka.", 'error')
        #     return jsonify({'success': False, 'message': "Please enter the taluka."}), 400
        # elif not state:
        #     flash("Please enter the state.", 'error')
        #     return jsonify({'success': False, 'message': "Please enter the state."}), 400
        elif not password:
            flash("Please enter a password.", 'error')
            return jsonify({'success': False, 'message': "Please enter a password."}), 400
        elif not image_url:
            flash("Please upload an image.", 'error')
            return jsonify({'success': False, 'message': "Please upload an image."}), 400
        
        #DAIRY INFROMATION
        elif not dairy_name:
            flash("Please enter the dairy name.", 'error')
            return jsonify({'success': False, 'message': "Please enter the dairy name."}), 400
        elif not  milk_storage_capacity:  # Use is None to check for 0 as valid input
            flash("Please enter the milk storage capacity.", 'error')
            return jsonify({'success': False, 'message': "Please enter the milk storage capacity."}), 400
        elif not address:
            flash("Please enter the address.", 'error')
            return jsonify({'success': False, 'message': "Please enter the address."}), 400
        
        #ACCOUNT INFORMATION
        elif not bank_name:
            flash("Please enter the bank name.", 'error')
            return jsonify({'success': False, 'message': "Please enter the bank name."}), 400
        elif not account_no:
            flash("Please enter the account number.", 'error')
            return jsonify({'success': False, 'message': "Please enter the account number."}), 400
        elif not branch_name:
            flash("Please enter the branch name.", 'error')
            return jsonify({'success': False, 'message': "Please enter the branch name."}), 400
        elif not ifsc_code:
            flash("Please enter the IFSC code.", 'error')
            return jsonify({'success': False, 'message': "Please enter the IFSC code."}), 400


        # Validate uniqueness for email, phone number, and account number
        if DairyOwner.query.filter_by(email=email).first():
            flash("Email already registered", 'error')
            return jsonify({'success': False, 'message': "Email already registered"}), 400

        if DairyOwner.query.filter_by(dairy_mobile_number=phone_number).first():
            flash("Phone number already exists", 'error')
            return jsonify({'success': False, 'message': "Phone number already exists"}), 400

        if DairyOwner.query.filter_by(account_no=account_no).first():
            flash("Account number already exists", 'error')
            return jsonify({'success': False, 'message': "Account number already exists"}), 400

        # Store form data in session for OTP validation
        session['dairyOwnerData'] = {
            "email": email,
            "owner_name": owner_name,
            "password": password,
            "food_license_no" : food_license_no,
            "dairy_name" : dairy_name,
            # "state" : state,
            # "district" : district,
            # "taluka" : taluka,
            # "village" : village,
            "phone_number": phone_number,
            "bank_name": bank_name,
            "account_no": account_no,
            "image_url": image_url,
            "milk_storage_capacity": milk_storage_capacity,
            "branch_name": branch_name,
            "ifsc_code": ifsc_code,
            "dob": dob,
            "address" : address
        }

        # Generate OTPs for email and mobile validation
        emailOTP = GenerateRandomOTP()
        mobileOTP = GenerateRandomOTP()
        session['email_otp'] = emailOTP
        session['mobile_otp'] = mobileOTP

        try:
            from app import mail
            # Simulate email OTP for development purposes
            print(f"Email OTP: {emailOTP}")
            print(f"Mobile OTP: {mobileOTP}")
            print(email)
            return jsonify({'success': True, 'message': "OTP sent successfully"}), 200
        except Exception as e:
            flash(f"Error in sending OTP: {str(e)}", 'error')
            return redirect(url_for('dairy_owner_register.mailError'))

    return render_template('dairyOwner/DairyOwnerRegister.html')

@dairy_owner_register.route('/dairyOwner/validate', methods=['GET', 'POST'])
def validateOTP():
    if request.method == 'POST':
        email_otp = request.form.get('email_otp')
        mobile_otp = request.form.get('mobile_otp')

        # Validate OTPs
        if int(email_otp) == int(session.get('email_otp')) and int(mobile_otp) == int(session.get('mobile_otp')):
            dairyOwner = session.get('dairyOwnerData')
            
            # Create new DairyOwner entry
            print(dairyOwner['milk_storage_capacity'])
            new_dairyOwner = DairyOwner(
                dairy_id = DairyOwner.generate_dairy_id(),
                dairy_name = dairyOwner['dairy_name'],
                owner_name = dairyOwner['owner_name'],
                email=dairyOwner['email'],
                password=bcrypt.hashpw(dairyOwner['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                address=dairyOwner['address'],
                dairy_mobile_number = dairyOwner['phone_number'],
                bank_name=dairyOwner['bank_name'],
                milk_storage_capacity=dairyOwner['milk_storage_capacity'],
                account_no=dairyOwner['account_no'],
                ifsc_code=dairyOwner['ifsc_code'],
                branch_name=dairyOwner['branch_name'],
                food_license_no = dairyOwner['food_license_no'],
                # state = dairyOwner['state'],
                # taluka = dairyOwner['taluka'],
                image_url = dairyOwner['image_url'],
                # village = dairyOwner['village'],
                # district = dairyOwner['district'],
                pending_payments = 0,
                total_payments = 0,
                dob=dairyOwner["dob"]
            )
            db.session.add(new_dairyOwner)
            db.session.commit()

            # Clear session data
            session.pop('email_otp')
            session.pop('mobile_otp')
            session.pop('dairyOwnerData')

            flash("Registration successful!", 'success')

            return jsonify({'success': True, 'message': "Registration successful!"}), 200

        flash("Invalid OTP", 'error')
        return jsonify({'success': False, 'message': "Invalid OTP"}), 400


    return render_template('dairyOwner/ValidateOTP.html')