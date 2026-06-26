import pandas as pd
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# List of all categories you need to process
categories = ['Plastic', 'Wooden', 'Food', 'Clothes', 'Furniture', 'Groceries']
filename_master = 'compliance datas collected for my key skills for decent compliance job(AutoRecovered).xlsx'

for category in categories:
    # 1. Extract data for the specific sheet
    try:
        df = pd.read_excel(filename_master, sheet_name=category, header=1)
    except Exception as e:
        print(f"Could not find sheet for {category}: {e}")
        continue # Skip to next category if sheet is missing

    all_zones = df['Geographic Zone'].dropna().unique()

    # 2. Batch Loop for Zones
    for zone in all_zones:
        regional_data = df[df['Geographic Zone'] == zone]
        
        pdf = FPDF(orientation='L')
        pdf.add_page()
        pdf.set_font("helvetica", size=10)
        
        pdf.cell(200, 10, text=f"Compliance Report: {zone} - {category}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
        
        # 3. Table Generation
        columns = ['Suburb / Node', 'Key Risk Category', 'Compliance Checklist / Metric', 'Requirements']
        with pdf.table(text_align="LEFT") as table:
            header_row = table.row()
            for col_name in columns: header_row.cell(col_name)
            for _, row_data in regional_data.iterrows():
                row = table.row()
                for col_name in columns:
                    row.cell(str(row_data.get(col_name, "")))
        
        filename = f"Report_{zone.replace(' ', '_')}_{category}.pdf"
        pdf.output(filename)
        print(f"Generated: {filename}")
