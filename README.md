# Automated-compliance-reporting-pipeline
An end-to-end Python automation pipeline that extracts multi-sector regional risk matrices from Excel, generates auditor-ready compliance PDFs, and handles secure distribution via SMTP.
# Automated Enterprise Compliance & Reporting Pipeline

An automated, end-to-end data engineering pipeline designed to streamline regional regulatory reporting. This system extracts compliance matrices from multi-sheet industrial datasets, transforms the raw parameters into auditor-ready localized PDF documents, and automates secure stakeholder distribution via SMTP.

## Key Features
* **Multi-Sector ETL Parsing:** Programmatically extracts and structures data across 6 distinct categories (Plastic, Food, Groceries, etc.) using `pandas`.
* **Dynamic PDF Generation:** Translates complex regional risk matrices into highly organized, consumer-ready compliance reports via `fpdf2`.
* **Automated Secure Distribution:** Features an integrated `smtplib` engine utilizing SSL layer authentication for batch email delivery.
* **GRC Focused Design:** Built to align with regional municipal frameworks (e.g., SE QLD Council parameters) to bridge the gap between technical automation and governance.

## Technologies Used
* **Language:** Python 3
* **Libraries:** Pandas, OpenPyXL, FPDF2, SMTPLib, EmailMessage
* **Data Sources:** Microsoft Excel
