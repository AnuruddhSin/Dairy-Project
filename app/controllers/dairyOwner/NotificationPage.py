from flask import Blueprint, session, redirect, url_for, render_template, flash
from app.models import Request, Farmer, db
from sqlalchemy import and_
dairy_owner_notification = Blueprint('dairy_owner_notification', __name__)

@dairy_owner_notification.route('/dairyOwner/dashboard/notification')
def viewNotifications():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    requests = Request.query.filter_by(dairy_id = session.get('dairy_id')).all()
    request_list = [item.as_dict() for item in requests]
    print(request_list)
    return render_template('dairyOwner/Notification.html', request_list = request_list)


@dairy_owner_notification.route('/dairyOwner/dashboard/notification/confirm/accept/farmer/<farmer_id>')
def confirmAcceptFarmer(farmer_id):
    farmer = Farmer.query.filter_by(farmer_id = farmer_id).first()
    return render_template('dairyOwner/ConfirmAddFarmer.html', farmer=farmer)

@dairy_owner_notification.route('/dairyOwner/dashboard/notification/accept/farmer/<farmer_id>')
def acceptFarmer(farmer_id):
    farmer = Farmer.query.filter_by(farmer_id = farmer_id).first()
    requests = Request.query.filter(and_(Request.farmer_id == farmer_id, Request.dairy_id == session.get('dairy_id'))).all()
    for request in requests:
        db.session.delete(request)
    farmer.dairy_id = session.get('dairy_id')
    db.session.commit()
    flash("Farmer Added To Dairy Successfully")
    return redirect(url_for('dairy_owner_notification.viewNotifications'))


@dairy_owner_notification.route('/dairyOwner/dashboard/notification/reject/farmer/<farmer_id>')
def rejectFarmer(farmer_id):
    requests = Request.query.filter(and_(Request.farmer_id == farmer_id, Request.dairy_id == session.get('dairy_id'))).all()
    for request in requests:
        db.session.delete(request)
    flash("Farmer Rejected Successfully")
    return redirect(url_for('dairy_owner_notification.viewNotifications'))