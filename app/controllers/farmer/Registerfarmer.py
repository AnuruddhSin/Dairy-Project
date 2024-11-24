from flask import Blueprint, redirect, render_template, url_for, session, request, flash, jsonify
from flask_mail import Message
from datetime import datetime
from flask import current_app as app 
from app.models import Farmer, Cow
from .generate_otp import GenerateRandomOTP

import cloudinary.uploader


farmer_reg_bp = Blueprint("farmer_register", __name__)


# Request Password Tested Working Properly
@farmer_reg_bp.route("/farmer/register", methods=["GET", "POST"])
def farmer_register():
    if request.method == "POST":
        from app import mail
        
        # Basic INFO of farmer
        fullname = request.form.get('fullname')
        print(fullname)
        

        farmer_id = request.form.get('farmer_id')
        phone_number = request.form.get("mobile_number")
        print(phone_number)
        email = request.form.get("email")
        print(email)
        dob = request.form.get("dob")
        print(dob)
        state = request.form.get('state')
        aadhar_no = request.form.get('aadhar_no')
        district = request.form.get('district')
        pincode = request.form.get('pincode')
        village = request.form.get('village')
        taluka =  request.form.get('taluka')
        image = request.files.get("profile_image")

        # Farm Details
        farm_name = request.form.get('farm_name')
        farm_address = request.form.get('farm_address')

        # Upload image to Cloudinary
        

        dob_date = datetime.strptime(dob, '%Y-%m-%d')  # Adjust format as per your input (e.g., 'YYYY-MM-DD')
    
    # Calculate the age
        today = datetime.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    
    # Check if age is less than 16
        if age < 16:
            flash("You must be at least 16 years old to register.", "error")
            return jsonify({'success': False, 'message': 'You must be at least 16 years old to register.'}), 400
        # Deleted the farm name object from the form

        address = request.form.get("address")
        print(address)
        password = request.form.get("password") 
        print(password)
        confirm_password = request.form.get('confirm_password')
        print(confirm_password)
        if(password != confirm_password):
            flash("Password Not Matching Please enter same password in confirm password", 'error')
            return jsonify({'success': False, 'message': "Password Not Matching Please enter same password in confirm password"}), 400

        # Farm Info
        
        
        # cattle_names = request.form.getlist('cattle_name')
        # breeds = request.form.getlist('breed')
        # ages = request.form.getlist('age')
        # milk_yields = request.form.getlist('milk_yield')
        # health_statuses = request.form.getlist('health_status')

        # Farmer Bank Info
        bank_name = request.form.get("bank_name")
        print(bank_name)
        account_no = request.form.get("account_no")
        print(account_no)
        branch_name = request.form.get("branch_name")
        print(branch_name)
        ifsc_code = request.form.get("ifsc_code")
        print(ifsc_code)
        # if 'profile_image' in request.files and request.files['profile_image'].filename != '':
            
        #     profile_image = request.files.get('profile_image')
        #     print(f"Received file: {profile_image.filename} (size: {profile_image.content_length})")
        #     print(profile_image)
        #     try:
        #         print("Uploading Image")
        #         upload_result = cloudinary.uploader.upload(profile_image)
        #         print("Successfully Uploaded Image")
        #         photo_url = upload_result.get('url')  # Get the URL of the uploaded image
        #     except Exception as e:
        #         flash("Error uploading image to Cloudinary.")
        #         print(e)
        #         return jsonify({'success': False, 'message': "Error uploading image to Cloudinary: {}".format(str(e))}), 500
        # else:
        #     photo_url = None  # Default if no image is uploaded
        if image:
            result = cloudinary.uploader.upload(image)
            image_url = result.get('url')
            print(image_url)
        else:
            image_url = None
        print(image_url)
        # Checking if the user has filled all the data or not
        if not (fullname and phone_number and email and dob and bank_name and account_no and branch_name and ifsc_code and image_url):
            flash("Please fill in all required fields.", "error")
            return jsonify({'success': False, 'message': "Please fill in all required fields."}), 400

        if Farmer.query.filter_by(farmer_email = email).first():
            flash("Email Already Registered", "error")
            return jsonify({'success': False, 'message': "Email Already Registered"}), 400
        
        if Farmer.query.filter_by(farmer_mobile_number = phone_number).first():
            flash("Phone no Already Registered", "error")
            return jsonify({'success': False, 'message': "Phone no Already Registered"}), 400
        
        

        if Farmer.query.filter_by(farmer_account_no = account_no).first():
            flash("Farmer Account Number already registered", "error")
            return jsonify({'success': False, 'message': "Farmer Account Number already registered"}), 400
        print(request.form)
        print(request.files)
        # Handle Cloudinary image upload for profile picture or cattle image
        # if request.files['profile_image']:
        

        # Storing the data in session to insert the data after validation
        session['farmer_data'] = {
            "farmer_id" : farmer_id,
            "farmer_name" : fullname,
            "password": password,
            "mobile_number": phone_number,
            "email": email,
            "dob": dob,
            # "cattle_names": cattle_names,
            # "breeds": breeds,
            # "ages": ages,
            # "milk_yields": milk_yields,
            # "health_statuses": health_statuses,
            "district" : district,
            "pincode" : pincode,
            "village" : village,
            "state" : state,
            "taluka" : taluka,
            "aadhar_no" : aadhar_no,
            "account_no": account_no,
            "bank_name": bank_name,
            "branch_name": branch_name,
            "ifsc_code": ifsc_code,
            "photo_url": image_url,  # Save the image URL to the session data
            "farm_name" : farm_name,
            "farm_address" : farm_address
        }

        # Generating OTP 
        email_otp = GenerateRandomOTP()
        mobile_otp = GenerateRandomOTP()
        session['email_otp'] = email_otp
        session['mobile_otp'] = mobile_otp
        session['email'] = email

        # Send OTP email

        # Error handling if mail not sent
        try:
            # msg = Message('Your OTP Code is:', recipients=[email])
            # msg.body = f"Your OTP is {email_otp}. Please enter it to complete your registration."
            # mail.send(msg)

            print("otp for mobile number:- ", mobile_otp)
            print("otp for email :- ", email_otp)
            return jsonify({'success': True, 'message': "OTP sent Successfully"}), 200
        except:
            return redirect('farmer_reg_bp.mailError')

    
    return render_template('farmer/farmer_register.html')


@farmer_reg_bp.route('/Mail Error')
def mailError():
    return render_template("mailError.html")