
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify, flash
from sqlalchemy import or_, and_, func, desc
from datetime import datetime, timedelta, date

from app.models import db, Farmer, DairyOwner, MilkTransaction, MilkEntry
from calendar import month_name
from app.models import db, Farmer, DairyOwner, MilkTransaction, MilkEntry, SupplyTransaction, Request

dairy_owner_dashboard = Blueprint('dairy_owner_dashboard', __name__)



# Route for Dairy Farmer Details
@dairy_owner_dashboard.route('/dairyOwner/Dashboard/farmer/details', methods=['GET', 'POST'])
def dairyFarmerDetails():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    dairy_owner = DairyOwner.query.filter_by(dairy_id=session.get('dairy_id')).first()
    if request.method == 'POST':
        if not session.get('dairy_id'):
            return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
        name = request.form.get('name')
        farmers = Farmer.query.filter(and_(
            Farmer.dairy_id == session.get('dairy_id'),  # Ensure the farmer belongs to the given dairy_id
            or_(Farmer.first_name.ilike(f"%{name}%"))  # Search by name
        )).all()
        farmers_list = [farmer.as_dict() for farmer in farmers]

        return render_template('dairyOwner/dairyFarmerDetails.html', farmers=farmers_list, dairy_owner=dairy_owner.as_dict())

    farmers = Farmer.query.filter_by(dairy_id=session.get('dairy_id')).all()
    farmer_list = [farmer.as_dict() for farmer in farmers]
    print(farmer_list)
    return render_template('dairyOwner/dairyFarmerDetails.html', farmers=farmer_list, dairy_owner=dairy_owner.as_dict())


# Route for milk Collection pie chart
@dairy_owner_dashboard.route('/dairyOwner/Dashboard/milk/collection')
def getMilkCollection():
    current_date = datetime.now()
    date = current_date.date()
    time = current_date.time()
    return render_template('dairyOwner/MilkCollection.html', date=date, time=time)


# Route for Dashboard
@dairy_owner_dashboard.route('/dairyOwner/Dashboard')
def dairyDashboard():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    #NOTE: set to specific date to show to graph
    # date = '2024-11-15'
    date = datetime.now().date()
    
    # Getting today's milk collection report
    today_transaction = MilkEntry.query.filter(
        and_(MilkEntry.dairy_id == session.get('dairy_id'),
            MilkEntry.collection_date == date
        )).all()
    dairy_owner = DairyOwner.query.filter_by(dairy_id = session.get('dairy_id')).first()
    total_farmers = dairy_owner.total_farmers
    print(total_farmers)
    # Logic for no of notifications
    notification_count = db.session.query(func.count(Request.farmer_id)).filter(Request.dairy_id == session.get('dairy_id')).scalar()
    
    total_today_milk = sum(entry.quantity_milk for entry in today_transaction)
    today_list = [item.as_dict() for item in today_transaction]
    print(len(today_list))
    print(today_list)
    if  today_list == None or total_farmers == None:
        percent_milk_collection = 0
        incomplete_collection = 0
        complete_collection = 0
    else:
        percent_milk_collection = "{:.2f}".format((len(today_list) / total_farmers) * 100)
        incomplete_collection = total_farmers - len(today_list)
        complete_collection = len(today_list)
    
        if len(today_list) > total_farmers:
            percent_milk_collection = 100
            incomplete_collection = 0
            complete_collection = total_farmers

    total_revenue = db.session.query(func.sum(SupplyTransaction.amount)).filter(SupplyTransaction.dairy_id == session.get('dairy_id')).scalar()
    
    transaction = MilkTransaction.query.filter_by(dairy_id=session.get('dairy_id')).order_by(desc(MilkTransaction.created_at)).all()
    dairy_owner = DairyOwner.query.filter_by(dairy_id = session.get('dairy_id')).first()
    transaction_list = [item.as_dict() for item in transaction]
    
    return render_template("dairyOwner/dairyDashboard.html", 
                           notification_count = notification_count,
                           total_revenue = total_revenue,
                           dairy_owner = dairy_owner, 
                           transactions = transaction_list, 
                           total_milk= total_today_milk, 
                           milk_percent = percent_milk_collection,
                           total_milk_collection = total_farmers,
                           incomplete_collection =  incomplete_collection,
                           complete_collection = complete_collection
                           )




# Function to get milk collection data
def get_milk_collection_data(start_date, end_date):
    milk_data = db.session.query(MilkEntry.milk_type, func.sum(MilkEntry.quantity_milk).label('quantity')) \
        .filter(MilkEntry.collection_date >= start_date, MilkEntry.collection_date <= end_date) \
        .group_by(MilkEntry.milk_type) \
        .all()
    
    # Convert the data into a dictionary format
    result = [{'milk_type': entry.milk_type, 'quantity': entry.quantity} for entry in milk_data]
    return result

# Milk Collection chart route
@dairy_owner_dashboard.route('/dairyOwner/Dashboard/milk/collection/chart', methods=["GET", "POST"])
def milk_collection_chart():
    date = request.args.get('date')

    if date == "null":
        date = datetime.today().strftime('%Y-%m-%d')
    view_type = request.args.get('viewType', 'daily')
    

    # Filter data based on the date and view type
    if date:
        selected_date = datetime.strptime(date, '%Y-%m-%d')
        if view_type == 'daily':
            # Code to fetch daily data
            start_date = selected_date
            end_date = selected_date
        elif view_type == 'weekly':
            # Code to fetch weekly data
            start_date = selected_date - timedelta(days=6)
            end_date = selected_date
        elif view_type == 'monthly':
            # Code to fetch monthly data
            start_date = selected_date.replace(day=1)
            end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        elif view_type == 'yearly':
            # Code to fetch yearly data
            start_date = selected_date.replace(month=1, day=1)
            end_date = selected_date.replace(month=12, day=31)
        
        # Fetch milk collection data from the database within the specified date range
        milk_data = get_milk_collection_data(start_date, end_date)

        # Extracting milk quantities by type for the pie chart
        cow_milk = sum(entry['quantity'] for entry in milk_data if entry['milk_type'] == 'cow')
        buffalo_milk = sum(entry['quantity'] for entry in milk_data if entry['milk_type'] == 'buffalo')
        goat_milk = sum(entry['quantity'] for entry in milk_data if entry['milk_type'] == 'goat')
        spoil_milk = sum(entry['quantity'] for entry in milk_data if entry['milk_type'] == 'spoil')
        west_milk = sum(entry['quantity'] for entry in milk_data if entry['milk_type'] == 'west')

        # Data to return: list of quantities for each milk type
        milk_quantities = [cow_milk, buffalo_milk, goat_milk, spoil_milk, west_milk]

        return jsonify(milk_quantities)

    # return jsonify([178, 116, 334, 234, 123])


# Route to search farmer Details event listener added 
# Route connected to dairy Farmer Details search bar 
# Event Listener added
@dairy_owner_dashboard.route('/search_farmer_details')
def search_farmer_details():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    farmers = Farmer.query.filter_by(dairy_id = session.get('dairy_id')).all()
    farmer_list = [item.as_dict() for item in farmers]
    query = request.args.get('query', '').lower()

    filtered_farmers = [
        farmer for farmer in farmer_list
        if query in farmer['farmer_name'].lower() or query in farmer['farmer_id'] or query in farmer['farmer_mobile_number'].lower()
    ]
    print(filtered_farmers)
    return jsonify(filtered_farmers)

@dairy_owner_dashboard.route("/dairyOwner/EditFarmer/<int:farmer_id>", methods=['GET', 'POST'])
def edit_farmer_details(farmer_id):
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    print("Route Called")
    farmer = Farmer.query.filter_by(farmer_id=str(farmer_id)).first()
    if not farmer:
        flash("Farmer not found.", "error")
        return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))  # Redirect back to farmer details page

    if request.method == "POST":
        # Update farmer details based on POST data from the modal form
        current_date = datetime.now().date()

        farmer.farmer_name = request.form.get('farmer_name')
        farmer.farmer_mobile_number = request.form.get('mobile_number')
        farmer.farmer_email = request.form.get('email')
        farmer.aadhar_no = request.form.get('aadhar_no')
        farmer.address = request.form.get("address")

        # Farmer Address Details
        farmer.state = request.form.get('state')
        farmer.district = request.form.get('district')
        farmer.taluka = request.form.get('taluka')
        farmer.village = request.form.get('village')
        farmer.pincode = request.form.get('pincode')

        # Farmer Bank Info
        farmer.bank_name = request.form.get("bank_name")
        farmer.account_no = request.form.get("account_no")
        farmer.branch_name = request.form.get("branch_name")
        farmer.ifsc_code = request.form.get("ifsc_code")
        farmer.updated_at = current_date
        # Commit changes to the database
        try:
            db.session.commit()
            return jsonify({"status": "success", "message": "Farmer details updated successfully."})  # Return JSON response
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": "Failed to update farmer details."})

    print(farmer)
    # For GET request, return the farmer data as JSON
    farmer_data = {
        "farmer_name": farmer.farmer_name,
        "mobile_number": farmer.farmer_mobile_number,
        "email": farmer.farmer_email,
        "aadhar_no": farmer.farmer_aadhar_no,
        "address": farmer.farm_address,
        "state": farmer.farmer_state,
        "district": farmer.farmer_district,
        "taluka": farmer.farmer_taluka,
        "village": farmer.farmer_village,
        "pincode": farmer.farmer_pincode,
        "bank_name": farmer.farmer_bank_name,
        "account_no": farmer.farmer_account_no,
        "branch_name": farmer.farmer_branch_name,
        "ifsc_code": farmer.farmer_ifsc_code
    }
    print("JSON data sent")
    return jsonify(farmer_data)  # Send the data as JSON to be used in the modal

@dairy_owner_dashboard.route('/dairyOwner/Dashboard/milk/collection/yearly', methods=['GET'])
def total_milk_by_month():
    # Get the year from the query parameters
    year = request.args.get('year', type=int)

    if not year:
        year = datetime.now().year

    # Query to get the total milk collection per month for the given year
    monthly_totals = db.session.query(
        func.extract('month', MilkEntry.collection_date).label('month'),
        func.sum(MilkEntry.quantity_milk).label('total_milk')
    ).filter(func.extract('year', MilkEntry.collection_date) == year) \
     .group_by(func.extract('month', MilkEntry.collection_date)) \
     .all()
    
    monthly_totals_dict = {int(month): total_milk for month, total_milk in monthly_totals}

    # Prepare the result for monthly totals
    result = []
    for month in range(1, 13):
        month_name_year = f"{month_name[month]} {year}"
        total_milk = monthly_totals_dict.get(month, 0)
        result.append({"month": month_name_year, "total": total_milk})
    
    # Return the data in the expected format
    return render_template("dairyOwner/MilkCollectionYearly.html" , months=result)

@dairy_owner_dashboard.route('/dairyOwner/Dashboard/milk/collection/yearly/pie', methods=['GET'])
def total_milk_by_type():
    # Get the year from the query parameters
    year = request.args.get('year', type=int)

    if not year:
        year = datetime.now().year

    # List of milk types in the required order
    milk_types = ['cow', 'buffalo', 'goat', 'spoil', 'west']

    # Query to get the total milk quantity per milk type for the given year
    milk_type_totals = db.session.query(
        MilkEntry.milk_type,
        func.sum(MilkEntry.quantity_milk).label('total_milk')
    ).filter(func.extract('year', MilkEntry.collection_date) == year) \
     .group_by(MilkEntry.milk_type).all()

    # Initialize a dictionary with zero values for each milk type
    milk_totals = {milk_type: 0 for milk_type in milk_types}

    # Populate the totals with the query results
    for milk_type, total_milk in milk_type_totals:
        if milk_type in milk_totals:
            milk_totals[milk_type] = total_milk

    # Return a list of totals in the required order
    result = [milk_totals[milk_type] for milk_type in milk_types]

    return jsonify(result)