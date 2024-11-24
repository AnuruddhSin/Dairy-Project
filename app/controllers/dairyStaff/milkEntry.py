from flask import Blueprint, render_template, request, redirect, url_for, session, make_response, flash
import traceback
from decimal import Decimal
import pdfkit
from datetime import date, datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.models import MilkEntry, Farmer, db, MilkTransaction, DairyOwner

milk_entry_bp = Blueprint('milk_entry_bp', __name__)

@milk_entry_bp.route('/milk_entry/<farmer_id>', methods=['GET', 'POST'])
def milk_entry(farmer_id):
    # Get farmer by ID
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    dairy_owner = DairyOwner.query.filter_by(dairy_id = session.get('dairy_id')).first()
    farmer = Farmer.query.filter_by(farmer_id=farmer_id).first()
    if not farmer:
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))  # Redirect to login if farmer not found

    if request.method == 'POST':
        try:
            # Capture form data
            collection_date = request.form.get('collection_date')
            time_str = request.form.get('collection_time')
            collection_time = datetime.strptime(time_str, "%H:%M").time()
            quantity_milk = request.form.get('quantity_milk')
            milk_type = request.form.get('milk_type')
            fat_content = request.form.get('fat_content')
            snf_content = request.form.get('snf_content')
            rate_per_l = request.form.get('rate_per_l')
            density = request.form.get('density')
            total_amount = request.form.get('total_amount')
            payment_status = request.form.get('payment_status')
            payment_method = request.form.get('payment_method')
            collected_by = request.form.get('collected_by')

            session['data'] = {
                "farmer_id": farmer.farmer_id,
                "farmer_name": farmer.farmer_name,
                "quantity_of_milk": quantity_milk,
                "milk_type": milk_type,
                "fat_content": fat_content,
                "solid_not_fat": snf_content,
                "rate_of_milk": rate_per_l,
                "density_of_milk": density,
                "total_amount": total_amount,
                "payment_status": payment_status,
                "payment_method": payment_method,
                "collected_by": collected_by
            }
            print(session.get('dairy_id'))
            dairy = DairyOwner.query.filter_by(dairy_id = session.get('dairy_id')).first()
            # Save the milk entry record to DB
            milk_entry = MilkEntry(
                farmer_id=farmer.farmer_id,
                collection_date=collection_date,
                collection_time=collection_time,
                quantity_milk=quantity_milk,
                milk_type=milk_type,
                fat_content=fat_content,
                snf_content=snf_content,
                rate_per_l=rate_per_l,
                bulk_supplier = dairy.dairy_name,
                total_amount=total_amount,
                payment_status=payment_status,
                payment_method=payment_method,
                collected_by=collected_by,
                dairy_id = session.get('dairy_id')
            )
            print(int(total_amount))
            farmer = Farmer.query.filter_by(farmer_id = farmer_id).first()
            print(payment_status)
            if payment_status == 'pending':
                if farmer.pending_payments == None:
                    farmer.pending_payments = Decimal(total_amount)
                farmer.pending_payments += Decimal(total_amount)
            elif payment_status == 'paid':
                if farmer.total_earnings == None:
                    farmer.total_earnings = Decimal(total_amount)
                farmer.total_earnings += Decimal(total_amount)
                milk_transaction = MilkTransaction(
                    farmer_name = farmer.farmer_name,
                    farmer_mobile_number = farmer.farmer_mobile_number,
                    time_added = datetime.now().time(),
                    milk_qty = quantity_milk,
                    fat = fat_content,
                    rate = rate_per_l,
                    total_amount = total_amount,
                    farmer_id = farmer.farmer_id,
                    dairy_id = session.get('dairy_id'),
                    created_at = datetime.now().date()
                )
                db.session.add(milk_transaction)
                
                print("Milk Transaction Added to DB")
            db.session.add(milk_entry)
            print(milk_entry)
            db.session.commit()
            flash(f"Milk Entry Successful for farmer {farmer.farmer_name}")
            return redirect(url_for('milk_entry_bp.success_milk_entry'))
        except Exception:
            traceback.print_exc()
            return "<h1>Server Error</h1>"

    # Pass the farmer object (including photo_url) to the template
    return render_template('dairyOwner/milkEntry.html', farmer=farmer, dairy_owner = dairy_owner)

@milk_entry_bp.route('/dairyOwner/successmilkentry')
def success_milk_entry():
    return render_template('dairyOwner/SuccessMilkEntry.html')

@milk_entry_bp.route('/dairyOwner/Download Milk Entry')
def downloadMilkEntry():
    data = session.get('data')
    now = datetime.today()
    date = now.date()
    current_time = now.time()
    time = current_time.strftime("%H:%M:%S")
    farmer_id = data['farmer_id']
    farmer = Farmer.query.filter_by(farmer_id = farmer_id).first()
    quantity = data['quantity_of_milk']
    milk_type = data['milk_type']
    avg_fat = data['fat_content']
    avg_snf = data['solid_not_fat']
    avg_rate = data['rate_of_milk']
    total_amount = data['total_amount']

    return render_template('dairyOwner/milkEntryBill.html', farmer=farmer, quantity=quantity, milk_type = milk_type, avg_fat = avg_fat, avg_snf = avg_snf, total_amount=total_amount,avg_rate = avg_rate, date=date, time=time)