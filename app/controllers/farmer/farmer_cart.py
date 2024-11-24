from flask import Blueprint, session, redirect, url_for, render_template, request, flash, jsonify
from app.models import Farmer, db, Cart, Delivery, Product 
from sqlalchemy import and_, func
import math
view_cart = Blueprint('view_cart', __name__)

@view_cart.route('/farmer/product/cart/view')
def viewCart():
    if not session.get('farmer_id'):
        return redirect(url_for('farmer_login_control.farmerLogin'))
    farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
    delivery_addresses = Delivery.query.filter_by(farmer_id = session.get('farmer_id')).all()
    addresses = [item.as_dict() for item in delivery_addresses]
    cart = Cart.query.filter_by(farmer_id = session.get('farmer_id')).all()
    items_list = [item.as_dict() for item in cart]
    total_price = sum(item.price * item.quantity for item in cart)
    gst = (total_price / 100)  * 20
    total_payable_amt = total_price + gst + 40
    # Remove the below print during deployment
    print(total_price)
    print("Addresses")
    print(addresses)
    print("Items list")
    print(items_list)
    return render_template('farmer/Products/YourCart.html', farmer= farmer, addresses = addresses, items = items_list, total_amount = total_price, gst = gst, total_payable_amt = total_payable_amt, math=math)


@view_cart.route('/farmer/product/cart/add/<product_id>', methods=['GET', 'POST'])
def addToCart(product_id):
    if not session.get('farmer_id'):
        return redirect(url_for('farmer_login_controler.farmerLogin'))
    
    quantity = 1
    # After implementing the ask quantity code remove the quantity var above and uncomment the below one
    # quantity = request.args.get('quantity')
    product_to_add = Product.query.filter_by(product_id = product_id).first()
    is_paid = False
    farmer_id = session.get('farmer_id')
    product = Cart.query.filter(and_(Cart.farmer_id == session.get('farmer_id'), Cart.product_id == product_id)).first()
    if product:
        
        product.quantity += 1
        db.session.commit()
        flash("Product already exists in cart increased the quantity by 1")
        return redirect(url_for('farmer_product.display_products'))

    else:    

        product = Cart(
            farmer_id = farmer_id,
            product_name = product_to_add.product_name,
            product_id = product_id,
            quantity = quantity,
            price = product_to_add.product_price,
            is_paid = is_paid
        )

        db.session.add(product)
        db.session.commit()
        flash("Product added to cart successfully")
        return redirect(url_for('farmer_product.display_products'))




@view_cart.route('/farmer/products/increase/quantity/<product_id>')
def increaseProductQuantity(product_id):
    if not session.get('farmer_id'):
        return redirect(url_for('farmer_login_control.farmerLogin'))
    
    product = Cart.query.filter(and_(Cart.product_id == product_id, Cart.farmer_id == session.get('farmer_id'))).first()

    product.quantity += 1
    db.session.commit()
    flash(f"Increased quantity of product {product.product_name} by 1")

    return redirect(url_for('view_cart.viewCart'))

@view_cart.route('/farmer/products/decrease/quantity/<product_id>')
def decreaseProductQuantity(product_id):
    if not session.get('farmer_id'):
        return redirect(url_for('farmer_login_control.farmerLogin'))
    
    product = Cart.query.filter(and_(Cart.farmer_id == session.get('farmer_id'), Cart.product_id == product_id)).first()

    if product.quantity == 1:
        db.session.delete(product)
        flash("Product Remove Successfully from Cart")
        db.session.commit()
        return redirect(url_for('view_cart.viewCart'))
        
    else:
        product.quantity -= 1
        db.session.commit()
        flash(f"Decreased the quantity of product {product.product_name} by 1")
        return redirect(url_for('view_cart.viewCart'))
    

@view_cart.route('/farmer/products/payment/gateway', methods=['GET', 'POST'])
def productGateway():
    if not session.get('farmer_id'):
        return redirect(url_for('farmer_login_control.farmerLogin'))
    if request.method == 'GET':
        farmer = Farmer.query.filter_by(farmer_id = session.get('farmer_id')).first()
        address_id = request.args.get('address_id')
        total_payable_amt = request.args.get('total_payable_amt')
        total_amount = request.args.get('total_amount')
        gst = request.args.get('gst')

        # Debugging: Print the retrieved parameters
        print("Address ID:", address_id)
        print("Total Payable Amount:", total_payable_amt)
        print("Total Amount:", total_amount)
        print("GST:", gst)
    
        return render_template('farmer/Products/FarmerCheckout.html', farmer=farmer)