from flask import Blueprint, session, redirect, render_template

dairy_owner_view_bp = Blueprint('dairy_owner_view_bp', __name__)

@dairy_owner_view_bp.route('/dairyOwner/view/bill/<BillId>')
def ViewDairyBill(BillId):
    BillId = BillId
    return render_template("dairyOwner/ViewBill", BillId=BillId)