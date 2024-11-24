from flask import Blueprint, redirect, url_for, render_template, session, request

payment_gateway_method = Blueprint("payment_gateway_method", __name__)

@payment_gateway_method.route('/payment/plan/<int:plan_no>',methods=['GET', 'POST'])
def payments(plan_no):
    
    if plan_no == 1:
        price = 199
        content = ["50 entries/month", "Access last 10 transactions", "can register upto 2 dairies", "can access up to 2 devices", "Access to support via email"]
    elif plan_no == 2:
        price = 399
        content = ["100 entries/month", "Access last 100 transactions", "can register upto 10 dairies", "can access up to 4 devices", "Faster response time via email"]
    elif plan_no == 3:
        price = 799
        content = ["Unlimited entries/month", "Access unlimited transactions", "can register upto 50 dairies", "can access up to 10 devices", "24/7 Premium Support"]
    else:
        return render_template('Error.html', error_msg = "Plan Selected must be invalid")
    print(price)
    print(content)
    return render_template('payment_gateway_plan.html', plan_no=plan_no, price=price, content= content)