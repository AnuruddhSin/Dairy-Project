from flask import Blueprint, render_template
from app.models import MilkEntry, db
from sqlalchemy import func
from datetime import datetime, timedelta

view_muster_bp = Blueprint("view_muster_bp", __name__)

@view_muster_bp.route('/dairyOwner/view/muster')
def ViewMuster():
    # Get the latest entry date
    latest_entry = db.session.query(func.max(MilkEntry.collection_date)).filter(MilkEntry.dairy_id == "OWN0025").scalar()
    print(latest_entry)
    if not latest_entry:
        return render_template('dairyOwner/ViewMuster.html', muster_data=[])

    # Calculate the start date (90 days before the latest entry to show more periods)
    start_date = latest_entry - timedelta(days=365)

    # Query to get all entries within the date range
    entries = (
        MilkEntry.query
        .filter(MilkEntry.dairy_id == "OWN0025")  # Replace with session['dairy_id'] when ready
        .filter(MilkEntry.collection_date.between(start_date, latest_entry))
        .order_by(MilkEntry.collection_date.desc())
        .all()
    )
    print(entries, "Milk Entries")
    # Group entries into 10-day ranges
    muster_data = []
    current_end_date = latest_entry

    while current_end_date >= start_date:
        # Define the current group's start date
        current_start_date = max(current_end_date - timedelta(days=9), start_date)

        # Filter entries that fall within the current group
        current_group = [entry for entry in entries if current_start_date <= entry.collection_date <= current_end_date]

        if current_group:
            # Calculate totals and averages for the current group
            total_milk = sum(entry.quantity_milk for entry in current_group)
            avg_fat = sum(entry.fat_content for entry in current_group) // len(current_group)
            avg_rate = sum(entry.rate_per_l for entry in current_group) // len(current_group)
            total_amount = sum(entry.total_amount for entry in current_group)

            group_data = {
                'start_date': current_start_date.strftime('%d/%m/%Y'),
                'end_date': current_end_date.strftime('%d/%m/%Y'),
                'total_milk': total_milk,
                'avg_fat': avg_fat,
                'avg_rate': avg_rate,
                'total_amount': total_amount,
                'entries': [{
                    'id': entry.id,
                    'time': entry.collection_time.strftime('%I:%M%p'),
                    'date': entry.collection_date.strftime('%d/%m/%Y'),
                    'milk': entry.quantity_milk,
                    'fat': entry.fat_content,
                    'rate': entry.rate_per_l,
                    'amount': entry.total_amount
                } for entry in current_group]
            }
            muster_data.append(group_data)
        
        # Move to the next group by decrementing the current end date
        current_end_date = current_start_date - timedelta(days=1)

    return render_template('dairyOwner/ViewMuster.html', muster_data=muster_data)
