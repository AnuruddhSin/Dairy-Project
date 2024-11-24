from flask import Blueprint, jsonify, session, request
from app.models import db, MilkTransaction, Farmer
from sqlalchemy.sql import func
from datetime import timedelta, datetime

farmer_milk_transaction_bp = Blueprint('milk_transaction', __name__)

# for testing purpose use http://127.0.0.1:5000/farmer/milk-transactions/10-days
@farmer_milk_transaction_bp.route('/farmer/milk-transactions/10-days', methods=['GET'])
def get_milk_transactions():
    
    farmer_id = session.get('farmer_id')
    if not farmer_id:
        return jsonify({"message": "Farmer not logged in"}), 401

    
    transactions = MilkTransaction.query.filter_by(farmer_id=farmer_id).order_by(MilkTransaction.created_at).all()

    if not transactions:
        return jsonify({"message": "No transactions found"}), 404

   
    grouped_data = []
    current_group = []
    group_start_date = transactions[0].created_at
    group_end_date = group_start_date + timedelta(days=9)

    for transaction in transactions:
        if group_start_date <= transaction.created_at <= group_end_date:
            current_group.append(transaction)
        else:
            
            if len(current_group) == 10:
                grouped_data.append(process_group(current_group, group_start_date, group_end_date))
            
            group_start_date = transaction.created_at
            group_end_date = group_start_date + timedelta(days=9)
            current_group = [transaction]

    
    if len(current_group) == 10:
        grouped_data.append(process_group(current_group, group_start_date, group_end_date))

    return jsonify(grouped_data), 200

def process_group(transactions, start_date, end_date):
    total_milk = sum(t.milk_qty for t in transactions)
    avg_fat = sum(float(t.fat) for t in transactions) / len(transactions)
    avg_rate = sum(float(t.rate) for t in transactions) / len(transactions)
    total_amount = sum(float(t.total_amount) for t in transactions)

    days_data = [
        {
            "transaction_id": t.transaction_id,
            "time_added": str(t.time_added),
            "date_added": str(t.created_at),
            "milk": t.milk_qty,
            "fat": float(t.fat),
            "rate": float(t.rate),
            "amount": float(t.total_amount),
        }
        for t in transactions
    ]

    return {
        "time_period": f"{start_date} - {end_date}",
        "total_milk_collection": total_milk,
        "avg_fat": avg_fat,
        "avg_rate": avg_rate,
        "total_amount": total_amount,
        "days": days_data,
    }

# for testing use http://127.0.0.1:5000/farmer/milk-transactions/range?start_date=2024-11-08&end_date=2024-11-17
@farmer_milk_transaction_bp.route('/farmer/milk-transactions/range', methods=['GET'])
def get_transactions_in_range():
    
    farmer_id = session.get('farmer_id')
    if not farmer_id:
        return jsonify({"message": "Farmer not logged in"}), 401

    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"message": "Both start_date and end_date are required"}), 400

    try:
        
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"message": "Invalid date format. Use YYYY-MM-DD"}), 400

    
    transactions = (
        MilkTransaction.query
        .filter(MilkTransaction.farmer_id == farmer_id)
        .filter(MilkTransaction.created_at.between(start_date, end_date))
        .order_by(MilkTransaction.created_at, MilkTransaction.time_added)
        .all()
    )

    if not transactions:
        return jsonify({"message": "No transactions found in the given date range"}), 404

    
    grouped_transactions = []
    for i in range(0, len(transactions), 10):
        group = transactions[i:i+10]
        if len(group) == 10:
            grouped_transactions.append(process_transaction_group(group))

    return jsonify(grouped_transactions), 200

def process_transaction_group(transactions):
    
    farmer = Farmer.query.filter_by(farmer_id=transactions[0].farmer_id).first()

    total_milk = sum(t.milk_qty for t in transactions)
    avg_fat = sum(float(t.fat) for t in transactions) / len(transactions)
    avg_rate = sum(float(t.rate) for t in transactions) / len(transactions)
    avg_snf = 0  
    total_amount = sum(float(t.total_amount) for t in transactions)

    
    last_transaction = transactions[-1]

    return {
        "farmer_id": farmer.farmer_id,
        "farmer_name": farmer.farmer_name,
        "address": farmer.farm_address,
        "contact_no": farmer.farmer_mobile_number,
        "date": str(last_transaction.created_at),
        "time": str(last_transaction.time_added),
        "total_milk": total_milk,
        "avg_fat": avg_fat,
        "avg_snf": avg_snf,  
        "avg_rate": avg_rate,
        "total_amount": total_amount
    }