from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.models import db, Product, DairyOwner, SupplyTransaction
import cloudinary.uploader
from datetime import datetime
from jinja2 import Undefined
from sqlalchemy import and_, or_, func, desc, extract

products = Blueprint('products', __name__)

@products.route('/dairyOwner/dashboard/view/products')
def viewProducts():
    if session.get("dairy_id") is None:
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    dairy_owner = DairyOwner.query.filter_by(dairy_id=session.get('dairy_id')).first()
    owner_name = dairy_owner.owner_name
    products = Product.query.filter_by(dairy_id=session.get('dairy_id')).all()
    product_list = [entries.as_dict() for entries in products]
    print(product_list)
    print(session.get('dairy_id'))
    def fix_undefined(data):
        if isinstance(data, Undefined):  # Check if data is of type Undefined
            return 0 # Return a default value, like None
        return data



    for product in product_list:
        product['product_number'] = fix_undefined(product.get('product_number', None))
    return render_template('dairyOwner/product1.html', owner_name=owner_name, products=product_list)


@products.route('/dairyOwner/dashboard/add/product', methods=['GET', 'POST'])
def addProducts():
    if session.get('dairy_id') is None:
        flash("Please Login before accessing other pages")
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    
    if request.method == 'POST':
        product_no = request.form.get('product_no')
        product_name = request.form.get("product_name")
        price = request.form.get('price')
        description = request.form.get('description')
        available_till = request.form.get('available')
        quantity = request.form.get('quantity')
        image = request.files.get('product_image')
        print(type(image))
        print(image)

        if image is None:
            flash("Please enter the product image to proceed")
            return redirect(url_for('products.addProducts'))
        # try:
        result = cloudinary.uploader.upload(image)
        image_url = result.get('url')
        new_product = Product(
        product_no = product_no,
        product_name = product_name,
        product_price = price,
        product_description = description,
        dairy_id = session.get('dairy_id'),
        available_till = available_till,
        quantity = quantity,
        image_url = image_url
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully")
        return redirect(url_for('products.viewProducts'))
        # except:
        #     return redirect(url_for('guest.DBError'))

    return render_template('dairyOwner/addproduct.html')


@products.route('/dairyOwner/dashboard/products/add/success')
def successAdd():
    return render_template('dairyOwner/SuccessProductAdd.html')



# Route for overview of all products sell history
@products.route('/dairyOwner/dashboard/products/sell/history')
def sellHistory():
    low_quantity_products = Product.query.filter(and_(Product.dairy_id == session.get('dairy_id'), Product.quantity <= 50)).all()
    low_prod_list = [item.as_dict() for item in low_quantity_products]
    most_purchased = db.session.query(
        SupplyTransaction.supply_id,
        func.sum(SupplyTransaction.quantity).label('total_quantity'),
        func.max(SupplyTransaction.transaction_date).label('last_transaction_date')
    ).group_by(SupplyTransaction.supply_id).order_by(func.sum(SupplyTransaction.quantity).desc()).limit(3).first()
    print(type(most_purchased))
    print(most_purchased)
    
    sold_prod = Product.query.filter_by(product_id = most_purchased[0]).first()
    print(sold_prod)
    sell_history = db.session.query(SupplyTransaction).order_by(desc(SupplyTransaction.transaction_date)).all()
    sell_list = [item.as_dict() for item in sell_history]
    print(sell_list)
    if not sold_prod:
        flash("No product has been sold to show most sold product data")
        return render_template('/dairyOwner/sellhistory.html', low_stock=low_prod_list, sellHistory = sell_list)
    
    # Return the data to the template
    return render_template('/dairyOwner/sellhistory.html', low_stock=low_prod_list, most_sold=most_purchased, most_sold_name = sold_prod.product_name, most_sold_stock_left = sold_prod.quantity, sellHistory = sell_list)





# Route for each product sell history
@products.route('/dairyOwner/dashboard/products/sell/<product_id>')
def productSell(product_id): 
    low_quantity_products = Product.query.filter(and_(Product.dairy_id == session.get('dairy_id'), Product.quantity <= 50)).all()
    low_prod_list = [item.as_dict() for item in low_quantity_products]
    most_purchased = db.session.query(
        SupplyTransaction.supply_id,
        func.sum(SupplyTransaction.quantity).label('total_quantity'),
        func.max(SupplyTransaction.transaction_date).label('last_transaction_date')
    ).group_by(SupplyTransaction.supply_id).order_by(func.sum(SupplyTransaction.quantity).desc()).limit(3).first()
    print(type(most_purchased))
    print(most_purchased)
    
    sold_prod = Product.query.filter_by(product_id = most_purchased[0]).first()
    

    sell_history = db.session.query(SupplyTransaction).order_by(desc(SupplyTransaction.transaction_date)).all()
    sell_list = [item.as_dict() for item in sell_history]
    print(sell_list)
    
    
    return render_template(
        '/dairyOwner/eachProductSellHistory.html',
        low_stock=low_prod_list,
        most_sold=most_purchased,
        most_sold_name=sold_prod.product_name if sold_prod else None,
        most_sold_stock_left=sold_prod.quantity if sold_prod else None,
        sellHistory=sell_list,
        product_id = product_id   
    )