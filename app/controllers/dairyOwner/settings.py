from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from app.models import DairyOwner, Request
from sqlalchemy import func
from app import db 

# Create Blueprint for settings route
dairy_settings = Blueprint("dairy_settings", __name__)

@dairy_settings.route('/dairyOwner/settings')
def settings():
    # Check if dairy_id is in session (user is logged in)
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))
    notification_count = db.session.query(func.count(Request.farmer_id)).filter(Request.dairy_id == session.get('dairy_id')).scalar()    
    # Get the dairy owner based on the session's dairy_id
    dairy_owner = DairyOwner.query.filter_by(dairy_id=session.get('dairy_id')).first()

    if not dairy_owner:
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))

    # Pass the dairy_owner to the template so it's available in settings.html
    return render_template('dairyOwner/settings.html', dairy_owner=dairy_owner, notification_count = notification_count)


@dairy_settings.route('/dairyOwner/update_profile', methods=['POST'])
def update_profile():
    if not session.get('dairy_id'):
        return jsonify({"error": "User not logged in"}), 401

    # Get the dairy owner based on the session's dairy_id
    dairy_owner = DairyOwner.query.filter_by(dairy_id=session.get('dairy_id')).first()

    if not dairy_owner:
        return jsonify({"error": "Dairy owner not found"}), 404

    # Get data from the request
    data = request.json
    dairy_owner.owner_name = data.get('fullName')
    dairy_owner.mobile_no = data.get('mobileNo')
    dairy_owner.email = data.get('email')
    dairy_owner.dob = data.get('dob')
    dairy_owner.food_license_no = data.get('foodLicenseNo')
    dairy_owner.udyam_aadhar_no = data.get('udyamAadharNo')
    dairy_owner.dairy_name = data.get('dairyName')
    dairy_owner.address = data.get('address')
    dairy_owner.bank_name = data.get('bankName')
    dairy_owner.account_no = data.get('accountNumber')
    dairy_owner.branch_name = data.get('branchName')
    dairy_owner.ifsc_code = data.get('ifscCode')
    

    # Commit the changes to the database
    try:
        db.session.commit()
        return jsonify({"success": "Profile updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update profile"}), 500
