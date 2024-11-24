from flask import Blueprint, render_template, redirect, url_for, session, jsonify
from app.models import DairyOwner
from app import db

dairy_profile = Blueprint("dairy_profile", __name__)

@dairy_profile.route('/dairyOwner/profile')
def view_profile():
    # Check if dairy_id is in session (user is logged in)
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))
    
    # Get the dairy owner based on the session's dairy_id
    dairy_owner = DairyOwner.query.filter_by(dairy_id=session.get('dairy_id')).first()

    if not dairy_owner:
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))

    # Return the profile details as JSON or render a template
    return render_template('dairyOwner/profile/profile.html', dairy_owner=dairy_owner)
