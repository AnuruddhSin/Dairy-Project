from flask import Blueprint, redirect, render_template, session, request, flash, url_for
from app.models import Farmer, db 
import bcrypt
from flask_bcrypt import check_password_hash, generate_password_hash

farmer_login_control = Blueprint("farmer_login_control", __name__)

@farmer_login_control.route("/farmer/login", methods=['GET', 'POST'])
def farmerLogin():
    if request.method == "POST":
        email_or_uid = request.form.get("emailoruid")
        password = request.form.get("password")
        print(email_or_uid, password)

        # Query the farmer by email
        farmer = Farmer.query.filter_by(farmer_email=email_or_uid).first()
        if farmer is None:
            farmer = Farmer.query.filter_by(farmer_id=email_or_uid).first()
            if farmer is None:
                flash("Farmer not found. Please check your credentials.", "error")
                return render_template('farmer/farmer_login.html')  # Render with flash message

        # Check if farmer exists and verify password
        if bcrypt.checkpw(password.encode('utf-8'), farmer.farmer_password.encode('utf-8')):
            session['farmer_id'] = farmer.farmer_id  # Store farmer ID in session
            flash("Login successful!", "success")
            return redirect(url_for('farmer_dashboard_bp.farmerDashboard'))  # Redirect to farmer dashboard
        else:
            flash("Invalid credentials. Please try again.", "error")
            return render_template('farmer/farmer_login.html')  # Render with error message
    
    return render_template('farmer/farmer_login.html')
