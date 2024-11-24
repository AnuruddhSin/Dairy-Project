from flask import Flask, request, jsonify, render_template, Blueprint, session, redirect, url_for, flash
from app.models import Farmer, db, Cow, ImportedFile, FileHistory
import pandas as pd
from sqlalchemy import func, desc, and_, cast, Date
from sqlalchemy.orm import sessionmaker
from app.models import MilkEntry, Farmer, Cow
from datetime import datetime, timedelta, date
import time

dairy_owner_excel = Blueprint('dairy_owner_excel', __name__)

@dairy_owner_excel.route('/dairyOwner/upload-excel', methods=['GET', 'POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        df = pd.read_excel(file, engine="calamine")
        # Rename all columns to lowercase
        df.columns = df.columns.str.lower()
        
        # Define the expected column names
        expected_columns = [
            'farmer name', 'farmer unique id', 'state', 'district', 'taluka', 'village',
            'animal unique id', 'animal type', 'cow type', 'gender', 'is milking', 'uploaded on', 'online verified',
            'online verification remark'
        ]

        # Check for missing or incorrect column names
        missing_columns = [col for col in expected_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({'error': f'Missing required columns: {", ".join(missing_columns)}'}), 400

        df = df[expected_columns]
        print(df.columns)

        columns_to_ignore = ["online verification remark"]
        missing_rows = df[df.drop(columns=columns_to_ignore).isnull().any(axis=1)]
        df.dropna(subset=[col for col in df.columns if col not in columns_to_ignore], inplace=True)
        ignored_ids = []
        accepted_ids = []

        for index, row in df.iterrows():
            if row['online verified'].lower() == "no":
                ignored_ids.append({
                    "Farmer Unique ID": row['farmer unique id'],
                    "Animal Unique ID": row['animal unique id'],
                    "Rejection message": row['online verification remark']
                })
            else:
                accepted_ids.append({
                    "animal_id": str(row['animal unique id']),
                    "farmer_name": row['farmer name'],
                    "farmer_id": str(row['farmer unique id']),
                    "state": row['state'],
                    "district": row['district'],
                    "taluka": row['taluka'],
                    "village": row['village'],
                    "animal_type": row['animal type'],
                    "cow_type": row['cow type'],
                    "gender": row['gender'],
                    "is_milking": row['is milking'].lower(),
                    "uploaded_on": row['uploaded on'],
                    "online_verified": row['online verified'].lower(),
                })
        for index, row in missing_rows.iterrows():
            data = {
                "Farmer Unique ID": row['farmer unique id'],
                "Animal Unique ID": row['animal unique id'],
                "Rejection message": row['online verification remark']
            }
            if data not in ignored_ids:
                data["Rejection message"] = row['online verification remark'] if not row['online verification remark'] else "Missing Values"
                ignored_ids.append(data)

        for cow in accepted_ids[:]:
            if cow["is_milking"] == "yes":
                cow["is_milking"] = True
            else:
                cow["is_milking"] = False
            if cow["online_verified"] == "yes":
                cow["online_verified"] = True
            else:
                cow["online_verified"] = False

            cow["uploaded_on"] = datetime.strptime(cow["uploaded_on"], '%d-%m-%Y %I:%M %p')

            farmer_exists = Farmer.query.filter_by(farmer_id=cow["farmer_id"]).first()
            if not farmer_exists:
                print(f"Skipping entry for animal_id {cow['animal_id']} as farmer_id {cow['farmer_id']} does not exist.")
                ignored_ids.append({
                    "Farmer Unique ID": cow["farmer_id"],
                    "Animal Unique ID": cow["animal_id"],
                    "Rejection message": "Farmer ID does not exist"
                })
                accepted_ids.remove(cow)
                continue  # Skip this cow entry if the farmer_id is missing

            # Check if animal_id already exists in the cow table
            animal_exists = Cow.query.filter_by(animal_id=cow["animal_id"]).first()
            if animal_exists:
                print(f"Skipping entry for animal_id {cow['animal_id']} as it already exists.")
                ignored_ids.append({
                    "Farmer Unique ID": cow["farmer_id"],
                    "Animal Unique ID": cow["animal_id"],
                    "Rejection message": "Animal ID already exists"
                })
                accepted_ids.remove(cow)
                continue  # Skip this cow entry if the animal_id is duplicate
            print(f"Adding entry for animal_id {cow['animal_id']} as farmer_id {cow['farmer_id']}")

            n_cow = Cow(
                animal_id = cow["animal_id"],
                farmer_name = cow["farmer_name"],
                farmer_id = cow["farmer_id"],
                state = cow["state"],
                district = cow["district"],
                taluka = cow["taluka"],
                village = cow['village'],
                animal_type = cow["animal_type"],
                cow_type = cow["cow_type"],
                gender = cow["gender"],
                is_milking = cow["is_milking"],
                uploaded_on = cow["uploaded_on"],
                online_verified = cow["online_verified"]
            )
            db.session.add(n_cow)
        db.session.commit()

        if accepted_ids:
            # Save file metadata to the database
            content = file.read()
            file_record = ImportedFile(f_name=file.filename, size=len(content) // 1024)  # Size in KB
            db.session.add(file_record)
            db.session.commit()

            for ids in accepted_ids:
                file_entry = FileHistory(
                    file_id = file_record.id,
                    uid = ids["animal_id"],
                    name = ids["farmer_name"],
                    type = ids["cow_type"]
                )
                db.session.add(file_entry)
            db.session.commit()
            return jsonify({'success': 'File uploaded successfully', 'file_id': file_record.id})
        
        else:
            return jsonify({'error': f'Data not imported as no farmer ID was registered Or Cows were already registered.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@dairy_owner_excel.route('/dairyOwner/file-history', methods=['GET'])
def file_history():
    files = ImportedFile.query.all()
    return jsonify([{'id': file.id, 'name': file.f_name, 'size': file.size} for file in files])
    # return jsonify([{'name': "testFile1", 'size': 126}, {'name': "testFile2", 'size': 126}])

@dairy_owner_excel.route('/dairyOwner/excel-import', methods=["GET"])
def excel():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    return render_template("dairyOwner/excel_import.html")

@dairy_owner_excel.route('/dairyOwner/excel/<data_type>/<timeframe>')
def showData(data_type, timeframe):
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    dairy_id = session.get('dairy_id')

    today = datetime.now().date()
    if timeframe == 'today':
        start_date = today
    elif timeframe == '10days':
        start_date = today - timedelta(days=10)
    elif timeframe == 'month':
        start_date = today - timedelta(days=30)
    elif timeframe == 'year':
        start_date = today - timedelta(days=365)
        print(start_date)
    else:
        flash("Invalid Time frame. Please select valid timeframe")
        return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))
    

    if data_type == 'muster':
        specific_columns = [
        "Payment Start Date", "Payment End Date", "District", "Taluka", "Village", 
        "Name of VLCC/Bulk Milk Supplier", "Farmer ID", "Name of Farmer", 
        "Total Quantity in Ltr.", "Average FAT", "Average SNF", 
        "Total Amount", "Average Rate per Ltr.", "Total Deductions if any", 
        "Net Payments", "Remark"
    ]

        query_columns = [
        MilkEntry.id.label("Entry ID"),  # Add the ID field to your query columns
        cast(MilkEntry.collection_date, Date).label("Payment Period From"),  
        cast(MilkEntry.collection_date + timedelta(days=10), Date).label("Payment Period To"),
        Farmer.farmer_district.label("District"),
        Farmer.farmer_taluka.label("Taluka"),
        Farmer.farmer_village.label("Village"),
        Farmer.farm_name.label("Name of VLCC/Bulk Milk Supplier"),
        Farmer.farmer_id.label("Farmer ID"),
        Farmer.farmer_name.label("Name of Farmer"),
        db.func.sum(MilkEntry.quantity_milk).label("Total Quantity in Ltr."),
        db.func.round(db.func.avg(MilkEntry.fat_content), 2).label("Average FAT"),  
        db.func.round(db.func.avg(MilkEntry.snf_content), 2).label("Average SNF"),  
        db.func.sum(MilkEntry.total_amount).label("Total Amount"),
        db.func.round(db.func.avg(MilkEntry.rate_per_l), 2).label("Average Rate per Ltr."),  
        db.literal(None).label("Total Deduction if any"),  
        db.func.sum(MilkEntry.total_amount).label("Net Payments"),
        db.literal("").label("Remarks")  
    ]

        query = (
            db.session.query(*query_columns)
            .join(Farmer, MilkEntry.farmer_id == Farmer.farmer_id)
            .filter(Farmer.dairy_id == dairy_id)
            .filter(MilkEntry.collection_date >= start_date)
            .group_by(
                MilkEntry.id,
                cast(MilkEntry.collection_date, Date),  
                cast(MilkEntry.collection_date + timedelta(days=10), Date),  
                Farmer.farmer_district,
                Farmer.farmer_taluka,
                Farmer.farmer_village,
                Farmer.farm_name,
                Farmer.farmer_id,
                Farmer.farmer_name
            )
            .order_by(cast(MilkEntry.collection_date, Date))  
        )


        data = query.all()

        serialized_data = [
            {
                column["name"]: str(getattr(row, column["name"])) if isinstance(getattr(row, column["name"]), (datetime, date))
                else getattr(row, column["name"])
                for column in query.column_descriptions
            }
            for row in data
        ]

        print(serialized_data)

        return jsonify(serialized_data)

    # Controller Logic for Farmer Bank Details

    if data_type == 'bankdetails':
        specific_columns = ["Farmer Name", "Farmer UID", "Farmer Email", "Mobile Number", "Bank Name", "Branch Name", "Account Number", "IFSC Code", "Total Earnings", "Pending Payments"]
        query = (
            db.session.query(
                Farmer.farmer_name,
                Farmer.farmer_id,
                Farmer.farmer_email,
                Farmer.farmer_mobile_number,
                Farmer.farmer_bank_name,
                Farmer.farmer_branch_name,
                Farmer.farmer_account_no,
                Farmer.farmer_ifsc_code,
                Farmer.total_earnings,
                Farmer.pending_payments
            )
            .filter(and_(Farmer.dairy_id == dairy_id, Farmer.created_at >= start_date))
        )
        data = query.all()

        if not data:
            flash("Something went wrong with fetching the data. Please contact the support")
            return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))
        
        
        print(data)
        serialized_data = [
            {
                column["name"]: str(getattr(row, column["name"])) if isinstance(getattr(row, column["name"]), (datetime, date))
                else getattr(row, column["name"])
                for column in query.column_descriptions
            }
            for row in data
        ]
        return jsonify(serialized_data)
        
        
    # Controller Logic for Cattle Data Export 
    if data_type == 'cattle':
        specific_columns = ["Farmer Name", "Farmer Unique ID", "State", "District", "Taluka", "Village", "Address", "Animal Unique ID", "Animal Type", "Cow Type", "Gender", "Is Milking", "Uploaded On", "Online Verification Remark", "Online Verified", "Created By System"]
        
        
        query = (
        db.session.query(
            Farmer.farmer_name,
            Farmer.farmer_id,
            Farmer.farmer_state,
            Farmer.farmer_district,
            Farmer.farmer_taluka,
            Farmer.farmer_village,
            Farmer.farm_address,
            Cow.animal_id,
            Cow.animal_type,
            Cow.cow_type,
            Cow.gender,
            Cow.is_milking,
            Cow.uploaded_on,
            Cow.online_remark,
            Cow.online_verified,
            db.literal("System").label("Created by System")
        )
        .join(Cow, Farmer.farmer_id == Cow.farmer_id)
        .filter(and_(Farmer.dairy_id == dairy_id, Cow.uploaded_on >= start_date))
        )

        data = query.all()

        if not data:
            flash("Cow data not found please contact support")
            return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))
        
        
        print(data)
        serialized_data = [
            {
                column["name"]: str(getattr(row, column["name"])) if isinstance(getattr(row, column["name"]), (datetime, date))
                else getattr(row, column["name"])
                for column in query.column_descriptions
            }
            for row in data
        ]
        return jsonify(serialized_data)
        
        

    # Controller Logic for Farmer Data to export with timeframes
    if data_type == "farmer":
        specific_columns = ["Farmer Name", "Farmer UID", "State", "District", "Taluka", "Village", "Address", "Total Cows", "Created At", "Updated At", "Aadhar Number", "Dairy ID"]
        
        query = db.session.query(
            Farmer.farmer_name,
            Farmer.farmer_id,
            Farmer.farmer_state,
            Farmer.farmer_district,
            Farmer.farmer_taluka,
            Farmer.farmer_village,
            Farmer.farm_address,
            Farmer.farmer_cows,
            Farmer.created_at,
            Farmer.updated_at,
            Farmer.farmer_aadhar_no,
            Farmer.dairy_id
        ).filter(Farmer.dairy_id == dairy_id)
        
        if start_date:
            query = query.filter(Farmer.created_at >= start_date)
        
        data = query.all()
        print("Printing data")
        print(data)
        if not data:
            flash("Farmer data not found please contact support")
            return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))

        serialized_data = [
            {
                column["name"]: str(getattr(row, column["name"])) if isinstance(getattr(row, column["name"]), (datetime, date))
                else getattr(row, column["name"])
                for column in query.column_descriptions
            }
            for row in data
        ]
        return jsonify(serialized_data)    
        
    

@dairy_owner_excel.route("/dairyOwner/show_file/<int:file_id>", methods=["GET", "POST"])
def show_file(file_id):
    data = FileHistory.query.filter_by(file_id=file_id).all()
    print("Rendering show_file template...")
    return render_template("dairyOwner/show_excel_import.html", data=data)

@dairy_owner_excel.route('/dairyOwner/search-file')
def search_file():
    query = request.args.get('query', '').lower()
    files = ImportedFile.query.filter(ImportedFile.f_name.ilike(f'%{query}%')).all()
    return jsonify([{'id': file.id, 'name': file.f_name, 'size': file.size} for file in files])

@dairy_owner_excel.route('/dairyOwner/delete-file/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    try:
        file_record = ImportedFile.query.get(file_id)
        if not file_record:
            return jsonify({'error': 'File not found'}), 404

        # Delete the associated file history records
        file_history_records = FileHistory.query.filter_by(file_id=file_id).all()
        for record in file_history_records:
            db.session.delete(record)

        # Delete the file record
        db.session.delete(file_record)
        db.session.commit()

        return jsonify({'success': 'File deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@dairy_owner_excel.route('/dairyOwner/edit/<data_type>/<entry_id>', methods=['POST'])
def edit_entry(data_type, entry_id):
    if not session.get('dairy_id'):
        return jsonify({"error": "Unauthorized access"}), 401
    print("Getting the route called")
    dairy_id = session.get('dairy_id')
    updated_data = request.json  # Updated data should be sent in JSON format
    print(updated_data)
    # try:
    if data_type == 'muster':
        # Fetch the MilkEntry and related Farmer data
        entry = db.session.query(MilkEntry).join(Farmer, MilkEntry.farmer_id == Farmer.farmer_id).filter(
            MilkEntry.id == entry_id,
            Farmer.dairy_id == dairy_id
        ).first()

        if not entry:
            return jsonify({"error": "Muster entry not found"}), 404

            # Update the entry fields
        if updated_data.get('Name of VLCC/Bulk Milk Supplier'):
            print(updated_data.get('Name of VLCC/Bulk Milk Supplier'))
        entry.quantity_milk = updated_data.get('quantity_milk', entry.quantity_milk)
        entry.fat_content = updated_data.get('fat_content', entry.fat_content)
        entry.snf_content = updated_data.get('snf_content', entry.snf_content)
        entry.total_amount = updated_data.get('total_amount', entry.total_amount)
        entry.rate_per_l = updated_data.get('rate_per_l', entry.rate_per_l)
        db.session.commit()
        flash("Muster Data updated successfully")
        return jsonify({"message": "Muster entry updated successfully"})

    elif data_type == 'bankdetails':
        # Fetch the Farmer data
        farmer = Farmer.query.filter_by(farmer_id=entry_id, dairy_id=dairy_id).first()
        if not farmer:
            return jsonify({"error": "Farmer bank details not found"}), 404
        print(updated_data.get('bank_name_name'))
        # Update the farmer's bank details
        farmer.farmer_name = updated_data.get('farmer_name', farmer.farmer_name)
        farmer.farmer_email = updated_data.get('farmer_email', farmer.farmer_email)
        farmer.farmer_id = updated_data.get('farmer_id', farmer.farmer_id)
        farmer.farmer_bank_name = updated_data.get('farmer_bank_name', farmer.farmer_bank_name)
        farmer.farmer_branch_name = updated_data.get('farmer_branch_name', farmer.farmer_branch_name)
        farmer.farmer_account_no = updated_data.get('farmer_account_no', farmer.farmer_account_no)
        farmer.farmer_ifsc_code = updated_data.get('farmer_ifsc_code', farmer.farmer_ifsc_code)
        farmer.total_earnings = updated_data.get("total_earnings", farmer.total_earnings)
        farmer.pending_payments = updated_data.get('pending_payments', farmer.pending_payments)
        db.session.commit()
        flash("Farmer Bank Details updated successfully")
        return jsonify({"message": "Farmer bank details updated successfully"})

    elif data_type == 'cattle':
        # Fetch the Cow entry
        print("Looking for cattle entry")
        cow = Cow.query.filter_by(animal_id=entry_id).join(Farmer, Cow.farmer_id == Farmer.farmer_id).filter(
            Farmer.dairy_id == dairy_id
        ).first()

        if not cow:
            print("Cattle not found")
            return jsonify({"error": "Cattle entry not found"}), 404
        print(updated_data.get('Online Verification Remark'))
        cow.online_remark = updated_data.get('Online Verification Remark')
        cow.animal_type = updated_data.get('animal_type', cow.animal_type)
        cow.cow_type = updated_data.get('cow_type', cow.cow_type)
        cow.gender = updated_data.get('gender', cow.gender)
        is_milking_str = updated_data.get('is_milking', cow.is_milking)
        if isinstance(is_milking_str, str):
            cow.is_milking = is_milking_str.lower() in ['true', '1', 'yes']
        else:
            cow.is_milking = bool(is_milking_str)
        db.session.commit()
        flash("Cattle Data updated successfully")
        return jsonify({"message": "Cattle entry updated successfully"})

    elif data_type == 'farmer':
        # Fetch the Farmer data
        farmer = Farmer.query.filter_by(farmer_id=entry_id, dairy_id=dairy_id).first()
        if not farmer:
            return jsonify({"error": "Farmer entry not found"}), 404

            # Update the farmer's details
        farmer.farmer_name = updated_data.get('farmer_name', farmer.farmer_name)
        farmer.farmer_state = updated_data.get('farmer_state', farmer.farmer_state)
        farmer.farmer_district = updated_data.get('farmer_district', farmer.farmer_district)
        farmer.farmer_taluka = updated_data.get('farmer_taluka', farmer.farmer_taluka)
        farmer.farmer_village = updated_data.get('farmer_village', farmer.farmer_village)
        farmer.farm_address = updated_data.get('farm_address', farmer.farm_address)
        farmer.farmer_cows = updated_data.get('farmer_cows', farmer.farmer_cows)
        farmer.farmer_aadhar_no = updated_data.get('farmer_aadhar_no', farmer.farmer_aadhar_no)
        db.session.commit()
        flash("Farmer Data updated successfully")
        return jsonify({"message": "Farmer entry updated successfully"})

    else:
        return jsonify({"error": "Invalid data type"}), 400

    # except Exception as e:
    #     db.session.rollback()
    #     return jsonify({"error": str(e)}), 500
