from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from app.models import Farmer, db, Cow, DairyOwner
from flask_mail import Message
from datetime import datetime
from .generate_otp import GenerateRandomOTP
import cloudinary.uploader
add_farmer_to_dairy = Blueprint('add_farmer_to_dairy', __name__)

# NOTE This route is similar to farmer Register because it contains same 

# Testing Complete functionality properly working and try except error handling remaining
@add_farmer_to_dairy.route("/dairyOwner/AddFarmer", methods=['GET', 'POST'])
def AddFarmer():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    now = datetime.now()
    current_time = f"{now.hour:02}:{now.minute:02}"
    today = datetime.today()
    dairy_id = session.get('dairy_id')
    dairy_owner = DairyOwner.query.filter_by(dairy_id=dairy_id).first()
    dairy_owner_list = dairy_owner.as_dict()
    current_date = today.strftime("%d-%m-%Y")
    
    if request.method == "POST":
        from app import mail
        # Basic INFO of farmer
        farmer_name = request.form.get('farmer_name')
        phone_number = request.form.get("mobile_number")
        email = request.form.get("email")
        # confirm_password = request.form.get('confirm_password')
        dob = request.form.get("dob")
        aadhar_no = request.form.get('aadhar_no')
        address = request.form.get("address")
        # password = request.form.get("password") 
        # Farm Info
        # cattle_no = request.form.get("no_of_cattle")
        # cattle_uids = request.form.getlist("cattle")
        # cattle_names = request.form.getlist('cattle_name')
        # breeds = request.form.getlist('breed')
        # ages = request.form.getlist('age')
        # milk_yields = request.form.getlist('milk_yield')
        # health_statuses = request.form.getlist('health_status')
        
        # Farmer Address Dets
        state = request.form.get('state')
        district = request.form.get('district')
        taluka = request.form.get('taluka')
        village = request.form.get('village')
        pincode = request.form.get('pincode')

        
        # Farmer Bank Info
        bank_name = request.form.get("bank_name")
        account_no = request.form.get("account_no")
        branch_name = request.form.get("branch_name")
        ifsc_code = request.form.get("ifsc_code")
        
        # Profile Image
        profile_image = request.files.get("profile_image")

        dob_date = datetime.strptime(dob, '%Y-%m-%d')  

        # if password != confirm_password:
        #     flash('Password Does Not match confirm password')
        #     return redirect(url_for('add_farmer_to_dairy.AddFarmer'))
    # Calculate the age
        today = datetime.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    
    # Check if age is less than 16
        if age < 16:
            flash("You must be at least 16 years old to register.", "error")
            return redirect(url_for('add_farmer_to_dairy.AddFarmer'))

        if not (farmer_name and phone_number and email and dob and address and bank_name and account_no and branch_name and ifsc_code):
            print(farmer_name, dob, branch_name, account_no, phone_number, email, address, ifsc_code, bank_name )
            flash("Please fill in all required fields.")
            print("all fields not entered")
            return redirect(url_for('add_farmer_to_dairy.AddFarmer'))
        
        if Farmer.query.filter_by(farmer_email=email).first():
            flash("Email Already Registered")
            return redirect(url_for('add_farmer_to_dairy.AddFarmer'))
        
        if Farmer.query.filter_by(farmer_mobile_number=phone_number).first():
            flash("Phone number Already Registered")
            return redirect(url_for('add_farmer_to_dairy.AddFarmer'))
        
        # Check cattle UIDs and bank account number as before...

        # Save profile image to Cloudinary if uploaded
        # image_url = None
        # if profile_image:
        #     try:
        #         upload_result = cloudinary.uploader.upload(profile_image)
        #         image_url = upload_result['secure_url']
        #     except Exception as e:
        #         flash("Failed to upload image. Please try again.")
        #         return redirect(url_for('add_farmer_to_dairy.AddFarmer'))

        # Store the data in session to insert the data after validation
        session['farmer_data'] = {
            "dairy_id": dairy_id,
            "aadhar_no" : aadhar_no,
            "state" : state,
            "district" : district,
            "taluka" : taluka,
            "village" : village,
            "pincode" : pincode,
            "farmer_name" : farmer_name,
            # "password": password,
            "mobile_number": phone_number,
            "email": email,
            "dob": dob,
            "address": address,
            "account_no": account_no,
            "bank_name": bank_name,
            "branch_name": branch_name,
            "ifsc_code": ifsc_code,
            # "profile_image": image_url  # Store the image URL in session
        }

        # Generating OTP and sending email logic...
        email_otp = GenerateRandomOTP()
        mobile_otp = GenerateRandomOTP()
        session['email_otp'] = email_otp
        session['mobile_otp'] = mobile_otp
        session['email'] = email

        # Send OTP email...
        
        print(mobile_otp)
        print(email_otp)
            # return redirect(url_for('validate_farmer_to_dairy_bp.ValidateFarmerToDairy'))
        return redirect(url_for('validate_farmer_to_dairy_bp.ValidateFarmerToDairy'))
    
    return render_template('dairyOwner/addFarmertoDairy.html', time=current_time, date=current_date, dairy_owner=dairy_owner_list)