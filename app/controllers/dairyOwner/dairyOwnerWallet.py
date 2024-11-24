from flask import Blueprint, redirect, render_template, url_for, session, request, flash, Response
from app.models import DairyOwner, Payment, Farmer, db, MilkTransaction
from sqlalchemy import and_ , or_
from decimal import Decimal
dairy_wallet = Blueprint("dairy_wallet", __name__)

@dairy_wallet.route('/dairyOwner/wallet/view')
def view_wallet():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))
    
    dairyOwner = DairyOwner.query.filter_by(dairy_id=session.get('dairy_id')).first()
    payments_history = Payment.query.filter_by(dairy_id=session.get('dairy_id')).all()

    payment_list = [item.as_dict() for item in payments_history]
    current_balance = dairyOwner.wallet_balance

    return render_template('dairyOwner/Wallet/viewWallet.html', current_balance=current_balance, payments=payment_list)

@dairy_wallet.route('/dairyOwner/wallet/pay/farmer/bank', methods=['GET', 'POST'])
def payFromWallet():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))
    
    if request.method == 'POST':
        account_no = request.form.get("account_no")
        farmer_name_or_id = request.form.get('farmer_id')
        print(farmer_name_or_id)
        ifsc_code = request.form.get('ifsc_code')
        account_name = request.form.get('account_name')

        if not(account_no and ifsc_code and farmer_name_or_id):
            flash("Please enter Complete Details to proceed")
            return redirect(url_for('dairy_wallet.payFromWallet'))
        farmer = Farmer.query.filter_by(farmer_id = farmer_name_or_id).first()
        if not farmer:
            farmer = Farmer.query.filter_by(farmer_name = farmer_name_or_id).first()
        print(farmer)
        session['farmer_id'] = farmer.farmer_id
        session['farmer_name'] = farmer.farmer_name
        session['farmer_pending_payments'] = farmer.pending_payments
        print(farmer.farmer_name)
        session['account_no'] = account_no
        session['ifsc_code'] = ifsc_code
        session['account_name'] = account_name

        # Redirect to amount asking page
        return redirect(url_for('dairy_wallet.askAmount'))
    return render_template("dairyOwner/Wallet/payToFarmerBank.html")


@dairy_wallet.route("/dairyOwner/wallet/pay/farmer/bank/amount", methods=['GET', 'POST'])
def askAmount():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))
    if request.method == 'POST':
        amount = request.form.get("amount")
        session['amount'] = amount
        session['method'] = 'Bank'
        session['type'] = 'Wallet'
        if not amount:
            flash("Please enter amount to proceed")
            return redirect(url_for('dairy_wallet.askAmount'))
        if amount > session.get('farmer_pending_payments') and not session.get('more_amount_confirmed'):
            return render_template('dairyOwner/wallet/confirmMorePayment.html', amount = amount, more_amount = amount - session.get('farmer_pending_payments'), pending_amount = session.get('farmer_pending_payments'), farmer_name = session.get('farmer_name'), farmer_id = session.get('farmer_id'))
        return render_template("dairyOwner/Wallet/confirmTransaction.html", amount=amount, farmer_name = session.get('farmer_name'), farmer_id = session.get("farmer_id"))
    return render_template("dairyOwner/Wallet/askAmountForBank.html")

@dairy_wallet.route('/dairyOwner/wallet/pay/farmer/bank/success')
def paymentSuccess():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login.dairyOwnerLogin'))
    session['more_amount_confirmed'] = False
    if session.get('method') == 'Bank':
        new_payment = Payment(
        dairy_id = session.get('dairy_id'),
        farmer_id = session.get('farmer_id'),
        farmer_name = session.get('farmer_name'),
        amount = session.get('amount'),
        method = 'Bank Transfer'
        )
        farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
        farmer.pending_payments -= Decimal(session.get('amount'))
        
        
        if (farmer.pending_payments - Decimal(session.get('amount') < 0)):
            # Add more amount will be paid logic to prevent overpaying
            pass
        
        
        db.session.add(new_payment)
        db.session.commit()
        transaction = Payment.query.filter(and_(Payment.dairy_id == session.get('dairy_id'),
                                                   Payment.amount == session.get('amount'),
                                                   Payment.method == 'Bank Transfer',
                                                   Payment.farmer_id == session.get('farmer_id'))).first()
        print(transaction.payment_id)
        flash("Transaction Successful")
    
    elif session.get('method') == 'UPI':
        # UPI Payment Logic Here


        # Adding Transaction to DB after success
        new_payment = Payment(
            dairy_id = session.get('dairy_id'),
            amount = session.get('amount'),
            farmer_id = session.get('farmer_id'),
            farmer_name = session.get('farmer_name'),
            method = 'UPI'
        )
        farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
        farmer.pending_payments -= Decimal(session.get('amount'))
       
       
       
       
        db.session.add(new_payment)
        db.session.commit()
        transaction = Payment.query.filter(and_(Payment.dairy_id ==session.get('dairy_id'),
                                                   Payment.amount == session.get('amount'),
                                                   Payment.method  == 'UPI'
        )).first()

        print(transaction.payment_id)
        flash("Transaction Successful")

    elif session.get('method') == 'Cash':
        # Adding cash transaction to DB
        new_payment = Payment(
            dairy_id = session.get('dairy_id'),
            amount = session.get('amount'),
            farmer_id = session.get('farmer_id'),
            farmer_name = session.get('farmer_name'),
            method = 'Cash'
        )
        farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
        


            
        farmer.pending_payments -= Decimal(session.get('amount'))
        db.session.add(new_payment)
        db.session.commit()
        transaction = Payment.query.filter(and_(Payment.dairy_id == session.get('dairy_id'),
                                                Payment.amount == session.get('amount'),
                                                Payment.farmer_id == session.get('farmer_id'),
                                                Payment.method == 'Cash')).first()
        print(transaction.payment_id)
        flash("Transaction Successful")

    return render_template('dairyOwner/Wallet/paymentSuccessToFarmer.html', transaction_id = transaction.payment_id)

@dairy_wallet.route('/dairyOwner/wallet/pay/farmer/upi', methods=['GET', 'POST'])
def payFromUpi():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    if request.method == 'POST':
        upi_id = request.form.get('upi_id')
        amount = request.form.get('amount')
        farmer_name_or_id = request.form.get('farmer_id')
        farmer = Farmer.query.filter_by(farmer_id = farmer_name_or_id).first()
        if not farmer:
            farmer = Farmer.query.filter_by(farmer_name = farmer_name_or_id).first()
        if not (upi_id or amount or farmer_name_or_id):
            flash("Please enter all details for payments")
            return redirect(url_for('dairy_wallet.payFromUpi'))
        print(farmer)
        session['farmer_id'] = farmer.farmer_id
        session['farmer_name'] = farmer.farmer_name
        session['method'] = 'UPI'
        session['amount'] = amount
        session['upi_id'] = upi_id
        print(amount)
        if Decimal(amount) > farmer.pending_payments and not session.get('more_amount_confirmed'):
            return redirect(url_for('dairy_wallet.confirmMorePayment'))
        
        else:
            return render_template('dairyOwner/Wallet/confirmTransaction.html', amount=amount, farmer_name = farmer.farmer_name, farmer_id = farmer.farmer_id)
    return render_template("dairyOwner/Wallet/payFarmerUPI.html")



@dairy_wallet.route('/dairyOwner/wallet/pay/farmer/cash/store', methods=['GET', 'POST'])
def payCash():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    if request.method == 'POST':
        farmer_id = request.form.get('farmer_id')
        amount = request.form.get('amount')
        farmer = Farmer.query.filter(and_(Farmer.farmer_id == farmer_id, Farmer.dairy_id == session.get('dairy_id'))).first()
        if not farmer:
            flash("Farmer id is invalid or the farmer may not be registered with your dairy")
            return redirect(url_for('dairy_wallet.view_wallet()'))
        if not(farmer_id or amount):
            flash("Please enter all details for payments")
            return redirect(url_for('dairy_wallet.payCash'))
        session['farmer_id'] = farmer_id
        session['farmer_name'] = farmer.farmer_name
        session['amount'] = amount
        session['method'] = 'Cash'
        if amount > farmer.pending_payments:
            return render_template('dairyOwner/wallet/confirmMorePayment.html', amount = amount, more_amount = amount - farmer.pending_payments, farmer_name = farmer.farmer_name, farmer_id = farmer.farmer_id)
        return render_template('dairyOwner/Wallet/confirmTransaction.html', amount=amount, farmer_name = farmer.farmer_name, farmer_id = farmer.farmer_id)



    return render_template('dairyOwner/Wallet/payFarmerCashStore.html')

@dairy_wallet.route('/dairyOwner/wallet/pay/farmer/cash/form', methods=['GET', 'POST'])
def payFromCash():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    if request.method == 'POST':
        id = request.form.get('id')
        amount = request.form.get('amount')

        farmer = Farmer.query.filter(and_(Farmer.farmer_id == id, Farmer.dairy_id == session.get('dairy_id'))).first()
        if not farmer:
            flash("Invalid Farmer id The farmer may not be registered with your dairy")
            return redirect(url_for('dairy_wallet.view_wallet'))
        if not(id or amount):
            flash("Please enter all details for payments")
            return redirect(url_for('dairy_wallet.payFromCash'))
        session['method'] = 'Cash'
        session['name_or_id'] = id
        session['amount'] = amount
        if amount > farmer.pending_payments:
            return render_template('dairyOwner/wallet/confirmMorePayment.html', amount = amount, more_amount = amount - farmer.pending_payments, farmer_name = farmer.farmer_name, farmer_id = farmer.farmer_id)
        return render_template('dairyOwner/Wallet/confirmTransaction.html')
    
    
@dairy_wallet.route('/dairyOwner/wallet/download')
def download_wallet_transactions():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.DairyOwnerLogin'))

    payments_history = Payment.query.filter_by(dairy_id=session.get('dairy_id')).all()
    
    # Create CSV data
    csv_data = "Transaction ID, Farmer ID, Farmer Name, Amount, Method, Date\n"
    for payment in payments_history:
        csv_data += f"{payment.payment_id}, {payment.farmer_id}, {payment.farmer_name}, {payment.amount}, {payment.method},\n"
    
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=wallet_transactions.csv"}
    )


@dairy_wallet.route('/confirm/more/payment', methods=['GET', 'POST'])
def confirmMorePayment():
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    amount = session.get('amount')
    farmer_id = session.get('farmer_id')
    farmer = Farmer.query.filter_by(farmer_id = farmer_id).first()
    return render_template('dairyOwner/wallet/confirmMorePayment.html', amount = amount, more_amount = Decimal(amount) - farmer.pending_payments, pending_amount= farmer.pending_payments, farmer_name = farmer.farmer_name, farmer_id = farmer.farmer_id)