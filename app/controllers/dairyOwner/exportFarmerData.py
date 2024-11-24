
from flask import Blueprint, session, redirect, url_for, Response, send_file, request, jsonify, current_app, flash
import pandas as pd
from io import StringIO, BytesIO
from sqlalchemy import and_ , func
from datetime import datetime, timedelta
from app.models import Farmer, DairyOwner, db, Cow, MilkEntry
from fpdf import FPDF

export_data = Blueprint('export_data', __name__)

    
@export_data.route('/dairyOwner/export/<data_type>/<timeframe>/<filename>')
def exportData(data_type, timeframe, filename):
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    choice = 'excel'
    dairy_id = session.get('dairy_id')
    today = datetime.now().date()
    if timeframe == 'today':
        start_date = today
    elif timeframe == '10days':
        start_date = today - timedelta(days=10)
    elif timeframe == 'month':
        start_date = today - timedelta(days=30)
    elif timeframe == 'year':
        start_date = today - timedelta(days=365)
        print(start_date)
    else:
        flash("Invalid Time frame. Please select valid timeframe")
        return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))
    

    # Controller Logic for Muster Data to export
    if data_type == 'muster':
        specific_columns = ["Payment Start Date", "Payment End Date", "District", "Taluka", "Village", "Name of VLCC/Bulk Milk Supplier", "Farmer ID", "Name of Farmer", "Total Quantity in Ltr.", "Average FAT", "Average SNF", "Total Amount", "Average Rate per Ltr.", "Total Deductions if any", "Net Payments", "Remark"]


        query_columns = [
            func.date_trunc('day', MilkEntry.collection_date).label("Payment Period From"),
            func.date_trunc('day', MilkEntry.collection_date + timedelta(days=10)).label("Payment Period To"),
            Farmer.farmer_district.label("District"),
            Farmer.farmer_taluka.label("Taluka"),
            Farmer.farmer_village.label("Village"),
            Farmer.farm_name.label("Name of VLCC/Bulk Milk Supplier"),
            Farmer.farmer_id.label("Farmer ID"),
            Farmer.farmer_name.label("Name of Farmer"),
            db.func.sum(MilkEntry.quantity_milk).label("Total Quantity in Ltr."),
            db.func.avg(MilkEntry.fat_content).label("Average FAT"),
            db.func.avg(MilkEntry.snf_content).label("Average SNF"),
            db.func.sum(MilkEntry.total_amount).label("Total Amount"),
            db.func.avg(MilkEntry.rate_per_l).label("Average Rate per Ltr."),
            db.literal(None).label("Total Deduction if any"),  # Placeholder
            db.func.sum(MilkEntry.total_amount).label("Net Payments"),
            db.literal("").label("Remarks")  # Placeholder
        ]

        query = (
            db.session.query(*query_columns)
            .join(Farmer, MilkEntry.farmer_id == Farmer.farmer_id)
            .filter(Farmer.dairy_id == dairy_id)
            .filter(MilkEntry.collection_date >= start_date)
            .group_by(
                func.date_trunc('day', MilkEntry.collection_date),  
                func.date_trunc('day', MilkEntry.collection_date + timedelta(days=10)),  
                Farmer.farmer_district,
                Farmer.farmer_taluka,
                Farmer.farmer_village,
                Farmer.farm_name,
                Farmer.farmer_id,
                Farmer.farmer_name
            )
            .order_by(func.date_trunc('day', MilkEntry.collection_date))  
        )


        data = query.all()

        # Export Excel File 
        if choice == 'excel':
            df = pd.DataFrame(data, columns=specific_columns)
            columns_to_round = [
                "Total Quantity in Ltr.",
                "Average FAT",
                "Average SNF",
                "Total Amount",
                "Average Rate per Ltr.",
                "Net Payments"
            ]
            for column in columns_to_round:
                if column in df.columns:
                    df[column] = pd.to_numeric(df[column], errors='coerce')
                    
            for col in df.select_dtypes(include=['datetime64[ns, UTC]', 'datetime64[ns]']):
                df[col] = df[col].dt.tz_localize(None)      
            date_columns = [
                "Payment Period From",  
                "Payment Period To"
            ]


            for column in date_columns:
                if column in df.columns:
                    df[column] = pd.to_datetime(df[column]).dt.date

            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index = False, sheet_name= 'Muster Data')

            output.seek(0)

            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment= True,
                download_name=f"{filename}.xlsx"
            )
        
       

    # Controller Logic for Farmer Bank Details

    if data_type == 'bankdetails':
        specific_columns = ["Farmer Name", "Farmer UID", "Farmer Email", "Mobile Number", "Bank Name", "Branch Name", "Account Number", "IFSC Code", "Total Earnings", "Pending Payments"]
        data = (
            db.session.query(
                Farmer.farmer_name,
                Farmer.farmer_id,
                Farmer.farmer_email,
                Farmer.farmer_mobile_number,
                Farmer.farmer_bank_name,
                Farmer.farmer_branch_name,
                Farmer.farmer_account_no,
                Farmer.farmer_ifsc_code,
                Farmer.total_earnings,
                Farmer.pending_payments
            )
            .filter(and_(Farmer.dairy_id == dairy_id, Farmer.created_at >= start_date))
            .all()
        )

        if not data:
            flash("Something went wrong with fetching the data. Please contact the support")
            return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))
        
        # Export Excel File
        if choice == 'excel':
            df = pd.DataFrame(data, columns=specific_columns)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index = False, sheet_name= 'Cattle Data')

            output.seek(0)

            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment= True,
                download_name=f"Farmer_Bank_Details_{timeframe}.xlsx"
            )
        
        




    # Controller Logic for Cattle Data Export 
    if data_type == 'cattle':
        specific_columns = ["Farmer Name", "Farmer Unique ID", "State", "District", "Taluka", "Village", "Address", "Animal Unique ID", "Animal Type", "Cow Type", "Gender", "Is Milking", "Uploaded On", "Online Verification Remark", "Online Verified", "Created By System"]
        
        
        data = (
        db.session.query(
            Farmer.farmer_name,
            Farmer.farmer_id,
            Farmer.farmer_state,
            Farmer.farmer_district,
            Farmer.farmer_taluka,
            Farmer.farmer_village,
            Farmer.farm_address,
            Cow.animal_id,
            Cow.animal_type,
            Cow.cow_type,
            Cow.gender,
            Cow.is_milking,
            Cow.uploaded_on,
            None,
            Cow.online_verified,
            None
        )
        .join(Cow, Farmer.farmer_id == Cow.farmer_id)
        .filter(and_(Farmer.dairy_id == dairy_id, Cow.uploaded_on >= start_date))
        .all()
        )

        if not data:
            flash("Cow data not found please contact support")
            return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))
        
        # Export Excel File
        if choice == 'excel':
            df = pd.DataFrame(data, columns=specific_columns)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index = False, sheet_name= 'Cattle Data')

            output.seek(0)

            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment= True,
                download_name=f"Cattle_Data_{timeframe}.xlsx"
            )
        
        



    # Controller Logic for Farmer Data to export with timeframes
    if data_type == "farmer":
        specific_columns = ["Farmer Name", "Farmer UID", "State", "District", "Taluka", "Village", "Address", "Total Cows", "Created At", "Updated At", "Aadhar Number", "Dairy ID"]
        
        query = db.session.query(
            Farmer.farmer_name,
            Farmer.farmer_id,
            Farmer.farmer_state,
            Farmer.farmer_district,
            Farmer.farmer_taluka,
            Farmer.farmer_village,
            Farmer.farm_address,
            Farmer.farmer_cows,
            Farmer.created_at,
            Farmer.updated_at,
            Farmer.farmer_aadhar_no,
            Farmer.dairy_id
        ).filter(Farmer.dairy_id == dairy_id)
        
        if start_date:
            query = query.filter(Farmer.created_at >= start_date)
        
        data = query.all()
        print("Printing data")
        print(data)
        if not data:
            flash("Farmer data not found please contact support")
            return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))

        
        # Export Excel File
        if choice == 'excel':
            df = pd.DataFrame(data, columns=specific_columns)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index = False, sheet_name= 'Farmer Data')

            output.seek(0)

            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment= True,
                download_name=f"Farmer_Data_{timeframe}.xlsx"
            )   
        
        

@export_data.route('/dairyOwner/export/<data_type>/<timeframe>/<choice>')
def exportData_in_choices(data_type, timeframe, choice):
    if not session.get('dairy_id'):
        return redirect(url_for('dairy_owner_login_bp.dairyOwnerLogin'))
    choice = 'excel'
    dairy_id = session.get('dairy_id')
    today = datetime.now().date()
    if timeframe == 'today':
        start_date = today
    elif timeframe == '10days':
        start_date = today - timedelta(days=10)
    elif timeframe == 'month':
        start_date = today - timedelta(days=30)
    elif timeframe == 'year':
        start_date = today - timedelta(days=365)
        print(start_date)
    else:
        flash("Invalid Time frame. Please select valid timeframe")
        return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))
    

    # Controller Logic for Muster Data to export
    if data_type == 'muster':
        specific_columns = ["Payment Start Date", "Payment End Date", "District", "Taluka", "Village", "Name of VLCC/Bulk Milk Supplier", "Farmer ID", "Name of Farmer", "Total Quantity in Ltr.", "Average FAT", "Average SNF", "Total Amount", "Average Rate per Ltr.", "Total Deductions if any", "Net Payments", "Remark"]


        query_columns = [
            func.date_trunc('day', MilkEntry.collection_date).label("Payment Period From"),
            func.date_trunc('day', MilkEntry.collection_date + timedelta(days=10)).label("Payment Period To"),
            Farmer.farmer_district.label("District"),
            Farmer.farmer_taluka.label("Taluka"),
            Farmer.farmer_village.label("Village"),
            Farmer.farm_name.label("Name of VLCC/Bulk Milk Supplier"),
            Farmer.farmer_id.label("Farmer ID"),
            Farmer.farmer_name.label("Name of Farmer"),
            db.func.sum(MilkEntry.quantity_milk).label("Total Quantity in Ltr."),
            db.func.avg(MilkEntry.fat_content).label("Average FAT"),
            db.func.avg(MilkEntry.snf_content).label("Average SNF"),
            db.func.sum(MilkEntry.total_amount).label("Total Amount"),
            db.func.avg(MilkEntry.rate_per_l).label("Average Rate per Ltr."),
            db.literal(None).label("Total Deduction if any"),  # Placeholder
            db.func.sum(MilkEntry.total_amount).label("Net Payments"),
            db.literal("").label("Remarks")  # Placeholder
        ]

        query = (
            db.session.query(*query_columns)
            .join(Farmer, MilkEntry.farmer_id == Farmer.farmer_id)
            .filter(Farmer.dairy_id == dairy_id)
            .filter(MilkEntry.collection_date >= start_date)
            .group_by(
                func.date_trunc('day', MilkEntry.collection_date),  
                func.date_trunc('day', MilkEntry.collection_date + timedelta(days=10)),  
                Farmer.farmer_district,
                Farmer.farmer_taluka,
                Farmer.farmer_village,
                Farmer.farm_name,
                Farmer.farmer_id,
                Farmer.farmer_name
            )
            .order_by(func.date_trunc('day', MilkEntry.collection_date))  
        )


        data = query.all()

        # Export Excel File 
        if choice == 'excel':
            df = pd.DataFrame(data, columns=specific_columns)
            columns_to_round = [
                "Total Quantity in Ltr.",
                "Average FAT",
                "Average SNF",
                "Total Amount",
                "Average Rate per Ltr.",
                "Net Payments"
            ]
            for column in columns_to_round:
                if column in df.columns:
                    df[column] = pd.to_numeric(df[column], errors='coerce')
                    
            for col in df.select_dtypes(include=['datetime64[ns, UTC]', 'datetime64[ns]']):
                df[col] = df[col].dt.tz_localize(None)      
            date_columns = [
                "Payment Period From",  
                "Payment Period To"
            ]


            for column in date_columns:
                if column in df.columns:
                    df[column] = pd.to_datetime(df[column]).dt.date

            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index = False, sheet_name= 'Muster Data')

            output.seek(0)

            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment= True,
                download_name=f"Muster_Data_{timeframe}.xlsx"
            )
        
        # Export CSV File
        if choice == 'csv':
            df = pd.DataFrame(data, columns=specific_columns)
            output = StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return Response(output, mimetype='text/csv', headers={"Content-Disposition" : "attachment;filename=Farmer_Bank_Detials.csv"})

        # Export PDF File
        if choice == 'pdf':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=6)
            page_width = pdf.w - 2 * pdf.l_margin

            num_cols = len(specific_columns)
            col_width = page_width / num_cols
            # Title
            pdf.cell(200, 10, txt='Farmer Data GauDhara', ln=True, align='C')

            # Heading Names
            for column in specific_columns:
                pdf.cell(col_width, 8, txt=column, border=1)
            pdf.ln()

            # Data
            for item in data:
                for value in item:
                    pdf.cell(col_width, 10, txt=str(value), border=1, align='C')
                pdf.ln()
    
            
            output = BytesIO()
            pdf_data = pdf.output(dest='S').encode('latin1') 
            output.write(pdf_data)
            output.seek(0)

            return send_file(output, mimetype='application/pdf', as_attachment=True, download_name="FarmerData.pdf")
        


    # Controller Logic for Farmer Bank Details

    if data_type == 'bankdetails':
        specific_columns = ["Farmer Name", "Farmer UID", "Farmer Email", "Mobile Number", "Bank Name", "Branch Name", "Account Number", "IFSC Code", "Total Earnings", "Pending Payments"]
        data = (
            db.session.query(
                Farmer.farmer_name,
                Farmer.farmer_id,
                Farmer.farmer_email,
                Farmer.farmer_mobile_number,
                Farmer.farmer_bank_name,
                Farmer.farmer_branch_name,
                Farmer.farmer_account_no,
                Farmer.farmer_ifsc_code,
                Farmer.total_earnings,
                Farmer.pending_payments
            )
            .filter(and_(Farmer.dairy_id == dairy_id, Farmer.created_at >= start_date))
            .all()
        )

        if not data:
            flash("Something went wrong with fetching the data. Please contact the support")
            return redirect(url_for('dairy_owner_dashboard.dairyFarmerDetails'))
        
        # Export Excel File
        if choice == 'excel':
            df = pd.DataFrame(data, columns=specific_columns)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index = False, sheet_name= 'Cattle Data')

            output.seek(0)

            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment= True,
                download_name=f"Farmer_Bank_Details_{timeframe}.xlsx"
            )
        
        # Export CSV File
        if choice == 'csv':
            df = pd.DataFrame(data, columns=specific_columns)
            output = StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return Response(output, mimetype='text/csv', headers={"Content-Disposition" : "attachment;filename=Farmer_Bank_Detials.csv"})


        # Export PDF file
        if choice == 'pdf':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=6)
            page_width = pdf.w - 2 * pdf.l_margin

            num_cols = len(specific_columns)
            col_width = page_width / num_cols
            # Title
            pdf.cell(200, 10, txt='Farmer Data GauDhara', ln=True, align='C')

            # Heading Names
            for column in specific_columns:
                pdf.cell(col_width, 8, txt=column, border=1)
            pdf.ln()

            # Data
            for item in data:
                for value in item:
                    pdf.cell(col_width, 10, txt=str(value), border=1, align='C')
                pdf.ln()
    
            
            output = BytesIO()
            pdf_data = pdf.output(dest='S').encode('latin1') 
            output.write(pdf_data)
            output.seek(0)

            return send_file(output, mimetype='application/pdf', as_attachment=True, download_name="FarmerData.pdf")
        




    # Controller Logic for Cattle Data Export 
    if data_type == 'cattle':
        specific_columns = ["Farmer Name", "Farmer Unique ID", "State", "District", "Taluka", "Village", "Address", "Animal Unique ID", "Animal Type", "Cow Type", "Gender", "Is Milking", "Uploaded On", "Online Verification Remark", "Online Verified", "Created By System"]
        
        
        data = (
        db.session.query(
            Farmer.farmer_name,
            Farmer.farmer_id,
            Farmer.farmer_state,
            Farmer.farmer_district,
            Farmer.farmer_taluka,
            Farmer.farmer_village,
            Farmer.farm_address,
            Cow.animal_id,
            Cow.animal_type,
            Cow.cow_type,
            Cow.gender,
            Cow.is_milking,
            Cow.uploaded_on,
            None,
            Cow.online_verified,
            None
        )
        .join(Cow, Farmer.farmer_id == Cow.farmer_id)
        .filter(and_(Farmer.dairy_id == dairy_id, Cow.uploaded_on >= start_date))
        .all()
        )

        if not data:
            flash("Cow data not found please contact support")
            return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))
        
        # Export Excel File
        if choice == 'excel':
            df = pd.DataFrame(data, columns=specific_columns)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index = False, sheet_name= 'Cattle Data')

            output.seek(0)

            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment= True,
                download_name=f"Cattle_Data_{timeframe}.xlsx"
            )
        
        # Export CSV File
        if choice == 'csv':
            df = pd.DataFrame(data, columns=specific_columns)
            output = StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return Response(output, mimetype='text/csv', headers={"Content-Disposition" : "attachment;filename=FarmerData.csv"})

        # Export PDF File
        if choice == 'pdf':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=6)
            page_width = pdf.w - 2 * pdf.l_margin

            num_cols = len(specific_columns)
            col_width = page_width / num_cols
            # Title
            pdf.cell(200, 10, txt='Farmer Data GauDhara', ln=True, align='C')

            # Heading Names
            for column in specific_columns:
                pdf.cell(col_width, 8, txt=column, border=1)
            pdf.ln()

            # Data
            for item in data:
                for value in item:
                    pdf.cell(col_width, 10, txt=str(value), border=1, align='C')
                pdf.ln()
    
            
            output = BytesIO()
            pdf_data = pdf.output(dest='S').encode('latin1') 
            output.write(pdf_data)
            output.seek(0)

            return send_file(output, mimetype='application/pdf', as_attachment=True, download_name="FarmerData.pdf")
    





    # Controller Logic for Farmer Data to export with timeframes
    if data_type == "farmer":
        specific_columns = ["Farmer Name", "Farmer UID", "State", "District", "Taluka", "Village", "Address", "Total Cows", "Created At", "Updated At", "Aadhar Number", "Dairy ID"]
        
        query = db.session.query(
            Farmer.farmer_name,
            Farmer.farmer_id,
            Farmer.farmer_state,
            Farmer.farmer_district,
            Farmer.farmer_taluka,
            Farmer.farmer_village,
            Farmer.farm_address,
            Farmer.farmer_cows,
            Farmer.created_at,
            Farmer.updated_at,
            Farmer.farmer_aadhar_no,
            Farmer.dairy_id
        ).filter(Farmer.dairy_id == dairy_id)
        
        if start_date:
            query = query.filter(Farmer.created_at >= start_date)
        
        data = query.all()
        print("Printing data")
        print(data)
        if not data:
            flash("Farmer data not found please contact support")
            return redirect(url_for('dairy_owner_dashboard.dairyDashboard'))

        # Export CSV File
        if choice == 'csv':
            df = pd.DataFrame(data, columns=specific_columns)
            output = StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return Response(output, mimetype='text/csv', headers={"Content-Disposition" : "attachment;filename=FarmerData.csv"})
        
        # Export Excel File
        if choice == 'excel':
            df = pd.DataFrame(data, columns=specific_columns)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index = False, sheet_name= 'Farmer Data')

            output.seek(0)

            return send_file(
                output,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment= True,
                download_name=f"Farmer_Data_{timeframe}.xlsx"
            )   
        
        # Export PDF File
        if choice == 'pdf':
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=6)
            page_width = pdf.w - 2 * pdf.l_margin

            num_cols = len(specific_columns)
            col_width = page_width / num_cols
        
            pdf.cell(200, 10, txt='Farmer Data GauDhara', ln=True, align='C')

            # Header name
            for column in specific_columns:
                pdf.cell(col_width, 8, txt=column, border=1)
            pdf.ln()

            # Data
            for item in data:
                for value in item:
                    pdf.cell(col_width, 10, txt=str(value), border=1, align='C')
                pdf.ln()
    
            
            output = BytesIO()
            pdf_data = pdf.output(dest='S').encode('latin1') 
            output.write(pdf_data)
            output.seek(0)

            return send_file(output, mimetype='application/pdf', as_attachment=True, download_name="FarmerData.pdf")


