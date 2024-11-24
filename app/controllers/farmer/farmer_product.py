from flask import Blueprint, render_template, session, redirect, url_for
from app.models import db, Product, Farmer

farmer_product_bp = Blueprint('farmer_product', __name__, template_folder='templates')

@farmer_product_bp.route('/farmer/products', methods=['GET'])
def display_products():
    
    farmer_id = session.get('farmer_id')

    if not farmer_id:
        
        return redirect(url_for('farmer_login_control.farmerLogin'))
    
    
    farmer = Farmer.query.filter_by(farmer_id=farmer_id).first()
    farmer_image_url = farmer.farmer_image_url
    if not farmer or not farmer.dairy_id:
        
        return "No products available", 404
    
   
    products = Product.query.filter_by(dairy_id=farmer.dairy_id).all()
    
    
    product_data = [product.as_dict() for product in products]
    
    
    return render_template('farmer/Products/FarmerProduct.html', products=product_data, farmer_image_url=farmer_image_url, farmer=farmer)


