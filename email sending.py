import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import smtplib
from email.message import EmailMessage

# --- CONFIGURATION ---
categories = ['Plastic', 'Wooden', 'Food', 'Clothes', 'Furniture', 'Groceries']
filename_master = 'compliance datas collected for my key skills for decent compliance job(AutoRecovered).xlsx'
sender_email = "your_email@gmail.com"
app_password = "YOUR_APP_PASSWORD_HERE" # Your 16-character App Password

def send_email(recipient, pdf_path, zone, category):
    msg = EmailMessage()
    msg['Subject'] = f"Compliance Report: {zone} - {category}"
    msg['From'] = sender_email
    msg['To'] = recipient
    msg.set_content(f"Attached is the automated compliance report for {zone} ({category}).")

    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=pdf_path)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            print(f"Successfully sent: {zone}")
    except Exception as e:
        print(f"Failed to send {zone}: {e}")

# --- MAIN LOOP ---
for category in categories:
    try:
        df = pd.read_excel(filename_master, sheet_name=category, header=1)
        all_zones = df['Geographic Zone'].dropna().unique()

        for zone in all_zones:
            regional_data = df[df['Geographic Zone'] == zone]
            
            filename = f"Report_{zone.replace(' ', '_')}_{category}.pdf"
            pdf = FPDF(orientation='L')
            pdf.add_page()
            pdf.set_font("helvetica", size=10)
            pdf.cell(200, 10, text=f"Report: {zone} - {category}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
            
            columns = ['Suburb / Node', 'Key Risk Category', 'Compliance Checklist / Metric', 'Requirements']
            with pdf.table(text_align="LEFT") as table:
                header_row = table.row()
                for col in columns: header_row.cell(col)
                for _, row_data in regional_data.iterrows():
                    row = table.row()
                    for col in columns: row.cell(str(row_data.get(col, "")))
            
            pdf.output(filename)
            # Change this recipient to your actual test email
            send_email("samihaanwarsuha@gmail.com", filename, zone, category)
            
    except Exception as e:
        print(f"Error processing category {category}: {e}")
