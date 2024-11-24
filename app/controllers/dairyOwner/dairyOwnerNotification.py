from flask import Blueprint, redirect, url_for, session, jsonify
from app.models import Request

dairy_notification = Blueprint("dairy_notification", __name__)

@dairy_notification.route('/dairyOwner/dashboard/notifications')
def showNotifications():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login.dairyOwnerLogin'))
    
    request_notification = Request.query.filter_by(dairy_id=session.get('dairy_id')).all()

    request_list = [items.as_dict() for items in request_notification]

    return jsonify(request_list)