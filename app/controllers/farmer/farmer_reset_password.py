from flask import Blueprint, redirect, render_template, session, request, make_response, jsonify, flash, url_for
from app.models import Farmer, db 
import bcrypt
from flask_bcrypt import check_password_hash, generate_password_hash
from .generate_otp import GenerateRandomOTP



# Farmer Reset Password Tested Working properly 

farmer_reset_password_bp = Blueprint("farmer_reset_password", __name__)

def send_otp(otp, mobile_number):
    pass

def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

# Request for Password Reset (uid or email, DOB, phone number)
@farmer_reset_password_bp.route("/farmer_request_reset", methods=["GET", "POST"])
def request_reset():
    if request.method == "POST":
        uid_or_email = request.form.get('uid_or_email')
        date_of_birth = request.form.get('date_of_birth')
        phone_number = request.form.get('phone_number')

        print("uid_or_email", uid_or_email) # Debug
        print("date_of_birth", date_of_birth) # Debug
        print("phone_number", phone_number) # Debug

        # Try to find the user by either UID or email
        # Determine if the input is an integer (UID) or a string (email)
        if is_integer(uid_or_email):
            # User provided UID
            farmer = Farmer.query.filter(
                Farmer.farmer_id == int(uid_or_email),
                Farmer.dob == date_of_birth,
                Farmer.phone_number == phone_number
            ).first()
        else:
            # User provided email
            farmer = Farmer.query.filter(
                Farmer.email == uid_or_email,
                Farmer.dob == date_of_birth,
                Farmer.phone_number == phone_number
            ).first()

        # if farmer exists
        if farmer:
            otp = GenerateRandomOTP()
            session["reset_data"] = {
                "uid_or_email": uid_or_email,
                "date_of_birth": date_of_birth,
                "phone_number": phone_number,
                "otp": otp
            }

            # send otp (incomplete)
            send_otp(otp=otp, mobile_number=phone_number)

            print(otp) # Debug

            flash("OTP sent successfully!!")
            return redirect(url_for("farmer_reset_password.reset_password"))

        flash("No user found with the details provided.")
        return redirect(url_for("farmer_reset_password.request_reset"))
    return render_template("farmer/farmer_password_reset_request.html")

@farmer_reset_password_bp.route("/farmer_reset_password", methods=["GET", "POST"])
def reset_password():
    # If no data in session, no need to be here. Go to Login page
    reset_data = session.get("reset_data")
    if not reset_data:
        return redirect(url_for("farmer_login_control.farmerLogin"))
    
    if request.method == "POST":
        received_otp = request.form.get('OTP', type=int)
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        uid_or_email = reset_data["uid_or_email"]
        date_of_birth = reset_data["date_of_birth"]
        phone_number = reset_data["phone_number"]

        otp = reset_data["otp"]

        print("uid_or_email", uid_or_email) # Debug
        print("date_of_birth", date_of_birth) # Debug
        print("phone_number", phone_number) # Debug
        print("received_otp", received_otp) # Debug
        print("otp", otp) # Debug
        print("new_password", new_password) # Debug
        print("confirm_password", confirm_password) # Debug

        # Try to find the user by either UID or email
        # Determine if the input is an integer (UID) or a string (email)
        if is_integer(uid_or_email):
            # User provided UID
            farmer = Farmer.query.filter(
                Farmer.farmer_id == int(uid_or_email),
                Farmer.dob == date_of_birth,
                Farmer.phone_number == phone_number
            ).first()
        else:
            # User provided email
            farmer = Farmer.query.filter(
                Farmer.email == uid_or_email,
                Farmer.dob == date_of_birth,
                Farmer.phone_number == phone_number
            ).first()
        
        # if farmer exist
        if farmer:
            # if otp matches
            if received_otp == otp:
                # same password then password will reset
                if new_password == confirm_password:

                    farmer.password = bcrypt.hashpw(confirm_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    db.session.commit()

                    session.pop("reset_data", None)

                    flash("Password Has been Reset Successfully.")
                    return redirect(url_for("farmer_login_control.farmerLogin"))
                
                flash("Password in the two fields not matching.")

            flash("Incorrect OTP. Please check and enter again")

    return render_template("farmer/farmer_password_reset_validate.html")


