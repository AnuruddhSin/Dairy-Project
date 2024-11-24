from flask import Blueprint, session, url_for, redirect, render_template, request, flash
from app.models import Cow, Farmer, db
from sqlalchemy import func
add_cattle = Blueprint('add_cattle', __name__)

@add_cattle.route('/farmer/dashboard/add/cattle', methods=['GET', 'POST'])
def addCattle():
    if not session.get('farmer_id'):
        return redirect(url_for('farmer_login_control.farmerLogin'))
    farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
    cattle_no = db.session.query(func.count(Cow.animal_id)).filter_by(farmer_id=session.get('farmer_id')).scalar()


    if request.method == 'POST':
        # Cattle no is dummy value it must be fetched from db i.e. exact no of cattle which the farmer is adding
        cattle_id = request.form.get('cattle_id')
        animal_type = request.form.get('animal_type')  
        print(cattle_id)
        print(animal_type)
        cattle_type = request.form.get('cattle_type')  
        print(cattle_type)
        farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
        print(farmer.farmer_name)
        new_cattle = Cow(
            farmer_name = farmer.farmer_name,
            farmer_id = farmer.farmer_id,
            animal_id = cattle_id,
            state = farmer.farmer_state,
            district = farmer.farmer_district,
            taluka = farmer.farmer_taluka,
            village = farmer.farmer_village,
            animal_type = animal_type,
            cow_type = cattle_type,
            gender = "Female",
            is_milking = True,
            online_verified = True
        )

        db.session.add(new_cattle)
        db.session.commit()

        flash(f"Added Cattle No {cattle_no} successfully to farmer profile")

    
    return render_template("farmer/cattle_section/AddCattle.html", farmer = farmer, cattle_no = cattle_no)
