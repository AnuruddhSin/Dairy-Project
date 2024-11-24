from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from app.models import db, Farmer, DairyOwner
from flask_mail import Message
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
guest = Blueprint("guest", __name__)

@guest.route('/')
def guestLanding():
    return render_template("LandingPage.html")

@guest.route('/pricing')
def guestPricingandPlans():
    return render_template("Pricing.html") #Pricing.html   temporary changed @aditya  #farmer/Dashboard/FarmerDashboard.html

@guest.route('/Contact_us', methods=['GET','POST'])
def contact_us():
    if request.method == 'POST':
        from app import mail
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        message = request.form.get("message")
        try:
            msg = Message('Your OTP Code is:', recipients=['atharvabhole239@gmail.com'])
            msg.body = f"FullName: {full_name} \n {message}"
            mail.send(msg)
            return redirect(url_for('guest.guestLanding'))
        except:
            return redirect(url_for('guest.mailError'))
    return render_template('Contact_us.html')

@guest.route('/support')
def guestSupport():
    return render_template("farmer/Products/FarmerCheckout.html")   #Support.html  #farmer/Dashboard/FarmerProfile.html

# Testing Complete loaded properly
@guest.route("/privacypolicy")
def guestPrivacyPolicy():
    return render_template("PrivacyPolicy.html")

# Testing complete loaded properly
@guest.route('/termsandconditions')
def guestTermsAndCondition():
    return render_template("TermsAndCondition.html")

@guest.route("/mail/error")
def mailError():
    return render_template("mailError.html")

# Testing Complete loaded properly
@guest.errorhandler(500)
def ServerError(error):
    return render_template('ServerError.html'), 500

# Testing Complete Loaded Properly
@guest.errorhandler(SQLAlchemyError)
def handle_db_error(error):
    error_message = str(error.__dict__.get('orig', 'An error occurred with the database.'))
    return render_template('DatabaseError.html', error_message=error_message), 500

@guest.route('/DB/error')
def DBError():
    return render_template("DatabaseError.html")

@guest.route('/logout')
def Logout():
    id = 0
    now = datetime.now()
    date = now.today()
    time = now.now()
    if not session.get('dairy_id'):
        id = session.get('farmer_id')
    else:
        id = session.get('dairy_id')
    return render_template("confirmLogout.html", user_id = id, date=date, time=time)

# @guest.route('/check_exists', methods=['GET'])
# def check_exists():
#     field = request.args.get('field')
#     value = request.args.get('value')

#     if field == "mobile_number":
#         exists = Farmer.query.filter_by(mobile_number=value).first() is not None
#     elif field == "email":
#         exists = Farmer.query.filter_by(email=value).first() is not None
#     elif field == 'account_no':
#         exists = FarmerBank.query.filter_by(account_no = value).first() is not None
#     else:
#         return jsonify({"error": "Invalid field"}), 400

#     return jsonify({"exists": exists})

@guest.route('/check_exists', methods=['GET'])
def check_exists():
    field = request.args.get('field')
    value = request.args.get('value')

    if field == "mobile_number":
        exists = Farmer.query.filter_by(phone_number=value).first() is not None
    elif field == "email":
        exists = Farmer.query.filter_by(email=value).first() is not None
    elif field == 'account_no':
        exists = Farmer.query.filter_by(farmer_account_no=value).first() is not None
    else:
        return jsonify({"error": "Invalid field"}), 400

    return jsonify({"exists": exists})


@guest.route('/check_exists_dairy_owner', methods=['GET'])
def check_exists_dairy_owner():
    field = request.args.get('field')
    value = request.args.get('value')

    if field == "mobile_number":
        exists = DairyOwner.query.filter_by(phone_number=value).first() is not None
    elif field == "email":
        exists = DairyOwner.query.filter_by(email=value).first() is not None
    elif field == 'account_no':
        exists = DairyOwner.query.filter_by(account_no=value).first() is not None
    else:
        return jsonify({"error": "Invalid field"}), 400

    return jsonify({"exists": exists})

@guest.route('/404/user/not/found')
def userNotFound():
    return render_template('userNotFound.html')

@guest.route('/redirect/to/dashboard')
def redirectToDashboard():
    if session.get('dairy_id'):
        return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))
    elif session.get('farmer_id') is not None:
        return redirect(url_for('farmer_dashboard_bp.farmerDashboard'))
    else:
        return redirect(url_for('farmer_login_control.farmerLogin'))
    
@guest.route('/confirmed/logout')
def confirmLogout():
    session.clear()
    return redirect(url_for('guest.guestLanding'))