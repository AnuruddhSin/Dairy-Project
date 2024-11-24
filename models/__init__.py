from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.cattle import Cow
from app.models.farmer import Farmer
from app.models.farmer_bank import FarmerBank
from app.models.milk_entry import MilkEntry
from app.models.payment import Payment
from app.models.supplies import Supplies
from app.models.supply_transactions import SupplyTransaction
from app.models.wallet import Wallet
from app.models.admin import Admin
from app.models.dairy_owner import DairyOwner
from app.models.transaction import Transaction
from app.models.milk_entry import MilkEntry
from app.models.dairy_owner_cattle import DairyOwnerCattle