# Farmer Folder Blueprints


# Controller for Login Page
from app.controllers.farmer import farmer_login_control

# Controller for validation of OTP
from app.controllers.farmer import farmer_validate

# Controller for Registration Page
from app.controllers.farmer import farmer_reg_bp

# Controller for Reset Password
from app.controllers.farmer import farmer_reset_password_bp

# Controller to display cattle data
from app.controllers.farmer import display_cattle

# Controller to add cattle in farmer data
from app.controllers.farmer import add_cattle

# Controller for displaying data of farmer dashboard
from app.controllers.farmer import farmer_dashboard_bp

# Controller to show farmer Milk Transaction data / Muster Data
from app.controllers.farmer import farmer_milk_transaction_bp

# Controller for farmer to purchase products
from app.controllers.farmer import farmer_product_bp


# Controller for farmer to add delivery address
from app.controllers.farmer import add_delivery_address

# Controller for farmer to view his cart
from app.controllers.farmer import view_cart







# Dairy Owner Folder Blueprints

# Controller to delete product from database of dairy owner
from app.controllers.dairyOwner import delete_product

# Controller for sales history graph and page NOTE : Also includes single product graph
from app.controllers.dairyOwner import sales_history

# Controller for dairy owner notification page 
from app.controllers.dairyOwner import dairy_owner_notification

# Controller for dairy Owner login page
from app.controllers.dairyOwner import dairy_owner_login_bp

# Controller for dairy owner register page
from app.controllers.dairyOwner import dairy_owner_register

# Controller for dairy owner to add farmer to his dairy / Register farmer through dairy owner portal
from app.controllers.dairyOwner import add_farmer_to_dairy

# Controller for showing all farmers list
from app.controllers.dairyOwner import list_farmers_bp

# Controller to view all farmers muster data
from app.controllers.dairyOwner import view_muster_bp

# Controller for dairy owner to show his products which are listed for purchases on portal

# Controller for dairy owner to show supplies sell history
# NOTE: Does not include graph 
from app.controllers.dairyOwner import supply_sell_history_bp

# Controller for dairy owner dashboard data
from app.controllers.dairyOwner import dairy_owner_dashboard

# Controller to validate farmer to dairy 
from app.controllers.dairyOwner import validate_farmer_to_dairy_bp

# Controller for dairy owner to reset his account password
from app.controllers.dairyOwner import dairyOwner_reset_password_bp

# Controller for dairy owner to view single farmer's profile
from app.controllers.dairyOwner import view_farmer

# Controller for dairy owner to show products page
from app.controllers.dairyOwner import products

# Controller for dairy owner to export data in excel format
from app.controllers.dairyOwner import export_data

# Controller for dairy owner to show wallet page and its contents
from app.controllers.dairyOwner import dairy_wallet

# Controller for excel page
from app.controllers.dairyOwner import dairy_owner_excel

# Controller for settings
from app.controllers.dairyOwner import dairy_settings

# Controller to join new farmer using farmer id
from app.controllers.dairyOwner import join_new_farmer

# Controller to delete a farmer from dairy database
from app.controllers.dairyOwner import delete_farmer

# Controller to view past farmers in dairy database
from app.controllers.dairyOwner import past_farmer

# Controller to show dairy report
from app.controllers.dairyOwner import dairy_report










# Base Folder Blueprints

# Controller to ask for payment gateway methods in SaaS model
from app.controllers.payment_gateway import payment_gateway_method

# Controller for static routes such as errors and static pages
from app.controllers.static_pages_controller import guest

# Controller for testing of frontend templates used by frontend team
# NOTE Remove this controller during deployment
from app.controllers.testing_controller import testing_blueprint