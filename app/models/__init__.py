from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.cows import Cow
from app.models.farmers import Farmer
from app.models.dairy_owner import DairyOwner
from app.models.products import Product
from app.models.milk_entry import MilkEntry
from app.models.supply_transactions import SupplyTransaction
from app.models.cart import Cart
from app.models.milk_transaction import MilkTransaction
from app.models.imported_files import ImportedFile
from app.models.farmer_req import Request
from app.models.wallet import Wallet
from app.models.payment_transaction import Payment
from app.models.pastFarmer import PastFarmer
from app.models.farmer_req import Request
from app.models.file_history import FileHistory
from app.models.delivery import Delivery