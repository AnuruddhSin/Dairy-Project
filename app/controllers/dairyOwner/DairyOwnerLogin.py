from flask import Blueprint, redirect, url_for, render_template, request, session, flash
import bcrypt
from app.models import DairyOwner

dairy_owner_login_bp = Blueprint('dairy_owner_login_bp', __name__)

@dairy_owner_login_bp.route('/dairyOwner/login', methods=['GET', 'POST'])
def dairyOwnerLogin():
    session.clear()  # Clear session data to prevent accidental reuse
    if request.method == 'POST':
        emailoruid = request.form.get('emailoruid')
        password = request.form.get('password')

        try:
            # Check for email or dairy_id in the database
            dairy_owner = DairyOwner.query.filter(
                (DairyOwner.email == emailoruid) | (DairyOwner.dairy_id == emailoruid)
            ).first()

            if not dairy_owner:
                flash("User not found", "error")
                return render_template('dairyOwner/dairy_owner_login.html')  # Render the page again
            
            # Check if the password matches
            if bcrypt.checkpw(password.encode('utf-8'), dairy_owner.password.encode('utf-8')):
                session['dairy_id'] = dairy_owner.dairy_id
                flash("Login Successful", "success")
                return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))  # Redirect on success
            else:
                flash("Invalid Credentials", "error")
                return render_template('dairyOwner/dairy_owner_login.html')  # Render the page again with the error message

        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return render_template('dairyOwner/dairy_owner_login.html')  # Render the page again if there's an error
    return render_template('dairyOwner/dairy_owner_login.html')
