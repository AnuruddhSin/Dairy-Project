from flask import Flask
from app.models import db
from flask_mail import Mail
import cloudinary
import cloudinary.uploader
import cloudinary.api
from app.controllers import guest, farmer_login_control, farmer_validate, farmer_reg_bp, farmer_reset_password_bp, dairy_owner_login_bp, farmer_dashboard_bp, farmer_milk_transaction_bp, farmer_product_bp
from app.controllers import dairy_owner_register, list_farmers_bp, add_farmer_to_dairy, view_muster_bp, supply_sell_history_bp, dairyOwner_reset_password_bp, payment_gateway_method
from app.controllers.dairyStaff.milkEntry import milk_entry_bp
from app.controllers.dairyOwner import  dairy_owner_dashboard, validate_farmer_to_dairy_bp, view_farmer, products, export_data, dairy_wallet, dairy_owner_excel, dairy_settings, dairy_profile
from app.controllers import testing_blueprint
from app.controllers.farmer import add_cattle, display_cattle, add_delivery_address, view_cart
from app.controllers.dairyOwner import join_new_farmer, delete_farmer, past_farmer, dairy_report, sales_history, dairy_owner_notification, delete_product
from dotenv import load_dotenv
import os

load_dotenv()
mail = Mail()

# Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Cloudinary Configuration
    cloudinary.config(
        cloud_name=os.getenv('CLOUD_NAME'),
        api_key=os.getenv('API_KEY'),
        api_secret=os.getenv('API_SECRET')
    )
    # Add the app.config here
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = os.getenv("MAIL_PORT")
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['TRACK_MODIFICATIONS'] = os.getenv('TRACK_MODIFICATIONS')
    app.config['TEMPLATES_AUTO_RELOAD'] = os.getenv("TEMPLATES_AUTO_RELOAD")


    # Initialize the external dependencies here    
    mail.init_app(app)
    db.init_app(app)

    # Register the Blueprints/Controllers here
    app.register_blueprint(guest)
    app.register_blueprint(farmer_login_control)
    app.register_blueprint(farmer_reg_bp)
    app.register_blueprint(farmer_validate)
    app.register_blueprint(farmer_reset_password_bp)
    app.register_blueprint(dairy_owner_login_bp)
    app.register_blueprint(dairy_owner_register)
    app.register_blueprint(list_farmers_bp)
    app.register_blueprint(milk_entry_bp)
    app.register_blueprint(add_farmer_to_dairy)
    app.register_blueprint(view_muster_bp)
    app.register_blueprint(supply_sell_history_bp)
    app.register_blueprint(dairy_owner_dashboard)
    app.register_blueprint(validate_farmer_to_dairy_bp)
    app.register_blueprint(dairyOwner_reset_password_bp)
    app.register_blueprint(farmer_dashboard_bp)
    app.register_blueprint(payment_gateway_method)
    app.register_blueprint(view_farmer)
    app.register_blueprint(products)
    app.register_blueprint(export_data)
    app.register_blueprint(delete_farmer)
    app.register_blueprint(dairy_wallet)
    app.register_blueprint(dairy_owner_excel)
    app.register_blueprint(join_new_farmer)
    app.register_blueprint(past_farmer)
    app.register_blueprint(dairy_settings)
    app.register_blueprint(dairy_report)
    app.register_blueprint(sales_history)
    app.register_blueprint(dairy_owner_notification)
    app.register_blueprint(dairy_profile)
    app.register_blueprint(display_cattle)
    app.register_blueprint(add_cattle)
    app.register_blueprint(testing_blueprint)
    app.register_blueprint(farmer_milk_transaction_bp)
    app.register_blueprint(farmer_product_bp) 
    app.register_blueprint(delete_product)
    app.register_blueprint(view_cart)
    app.register_blueprint(add_delivery_address)


    return app

