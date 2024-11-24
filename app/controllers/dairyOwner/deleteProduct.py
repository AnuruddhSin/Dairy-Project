from flask import Blueprint, session, redirect, url_for, flash, jsonify, request
from app.models import Product, db
delete_product = Blueprint('delete_product', __name__)


@delete_product.route('/dairyOwner/products/delete/product/<product_id>', methods=['DELETE'])
def deletProduct(product_id):
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))

    try:
        product = Product.query.get(product_id)
        if not product:
            flash("Product ID not found in database. Please select valid product")
            return jsonify({'error': "Product not found"}), 404
        
        db.session.delete(product)
        db.session.commit()
        flash("Product Deleted Successfully")
        return jsonify({"message" : "Product Deleted Successfully"}), 200

    except Exception as e:
        print(f"Error: {e}")
        db.session.rollback()
        flash("Internal server error occurred")
        return jsonify({"error": "An error occurred while deleting the product"}), 500
    
@delete_product.route('/dairyOwner/products/edit/product/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    # Get the product details from the request
    product_data = request.get_json()
    product = Product.query.filter_by(product_id = product_id).first()
    # Check if the product exists
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Update product in the database
    product.product_name = product_data['name'] or "None" if product_data['name'] is None else product_data['name']
    product.product_price = product_data['price'] or 99999 if product_data['price'] is None else product_data['price']
    product.product_description = product_data['description'] or 'No Description' if product_data['description'] is None else product_data['description']
    product.quantity = product_data['quantity'] or 0 if product_data['quantity'] is None else product_data['quantity']
    product.percent_discount = product_data['discount'] or 0 if product_data['discount'] is None else product_data['discount']
    product.product_no = product_data['product_no'] or 0 if product_data['product_no'] is None else product_data['product_no']
    db.session.commit()
    # Return success response
    return jsonify({'message': 'Product updated successfully'}), 200