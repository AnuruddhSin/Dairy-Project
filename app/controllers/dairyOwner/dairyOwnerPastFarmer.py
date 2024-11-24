from flask import Blueprint, redirect, render_template, url_for, session
from app.models import PastFarmer
past_farmer = Blueprint('past_farmer', __name__)

# @past_farmer.route('/dairyOwner/dashboard/view/past/farmers')
# def viewPastFarmer():
#     past_farmers_list = PastFarmer.query.filter_by(dairy_id = session.get('dairy_id')).all()

#     past_farmer = [item.as_dict() for item in past_farmers_list]
#     print(past_farmer)
#     for farmer in past_farmer:
#         if farmer.get('dairy_id') == session.get('dairy_id'):
#             past_farmer.remove(farmer)
#     print(past_farmer)
#     return render_template('dairyOwner/pastMembers.html', farmers = past_farmer)

@past_farmer.route('/dairyOwner/dashboard/view/past/farmers')
def viewPastFarmer():
    # Get the current dairy_id from the session
    current_dairy_id = session.get('dairy_id')

    # Query for past farmers whose dairy_id is not the current dairy_id
    past_farmers_list = PastFarmer.query.filter(PastFarmer.dairy_id == current_dairy_id).all()

    # Convert to dictionary representation for each farmer
    past_farmer = [item.as_dict() for item in past_farmers_list]

    print(past_farmer)  # For debugging
    return render_template('dairyOwner/pastMembers.html', farmers=past_farmer)
