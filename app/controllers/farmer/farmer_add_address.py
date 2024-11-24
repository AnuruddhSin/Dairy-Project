from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from app.models import Delivery, db, Farmer


add_delivery_address = Blueprint('add_delivery_address', __name__)

@add_delivery_address.route('/farmer/products/add/delivery/address', methods = ['GET', 'POST'])
def addAddress():
    if not session.get('farmer_id'):
        return redirect(url_for('farmer_login_control'))
    farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
    if request.method == 'POST':
        farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
        # Taking input all details to create delivery address entry in DB
        name = request.form.get('name')
        mobile_no = request.form.get('mobile_no')
        alternate_mobile_no = request.form.get('alternate_no')
        state = request.form.get('state')
        district = request.form.get('district')
        taluka = request.form.get('taluka')
        village = request.form.get('village')
        pincode = request.form.get('pincode')
        nearby_landmark = request.form.get('landmark')

        new_address = Delivery(
            farmer_id = session.get('farmer_id'),
            name = name,
            mobile_no = mobile_no,
            dairy_id = farmer.dairy_id,
            alternate_mobile_number = alternate_mobile_no,
            state = state,
            district = district,
            taluka = taluka,
            village = village,
            pincode = pincode,
            nearby_landmark = nearby_landmark
        )

        db.session.add(new_address)
        db.session.commit()

        flash("Delivery Address added successfully")
        return redirect(url_for('view_cart.viewCart'))

    return render_template('farmer/Products/NewAddress.html', farmer=farmer)
