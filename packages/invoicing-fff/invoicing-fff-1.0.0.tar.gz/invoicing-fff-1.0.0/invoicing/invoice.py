
import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path
import os


def generate(invoices_path, pdfs_path, image_path, company_name,
             product_id, product_name, amount_purchased, price_per_unit, total_price):

    """
    This function converts invoice Excel files into PDF invoices.

    :param invoices_path:
    :param pdfs_path:
    :param image_path:
    :param company_name:
    :param product_id:
    :param product_name:
    :param amount_purchased:
    :param price_per_unit:
    :param total_price:
    :return:
    """

    filepaths = glob.glob(f"{invoices_path}/*.xlsx")

    for filepath in filepaths:

        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=False, margin=0)

        pdf.add_page()

        filename = Path(filepath).stem
        invoice_nr, invoice_date = filename.split("-")

        # Add title
        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Invoice nr. : {invoice_nr}", ln=1)
        pdf.cell(w=50, h=8, txt=f"Date : {invoice_date}", ln=1)

        pdf.ln(5)

        df = pd.read_excel(filepath, sheet_name="Sheet 1")

        #  Add header
        columns = df.columns
        columns = [item.replace("_", " ").title() for item in columns]

        pdf.set_font(family="Times", size=14, style="B")
        pdf.set_text_color(40, 40, 40)
        pdf.cell(w=50, h=14, txt=columns[0], border=1)
        pdf.cell(w=70, h=14, txt=columns[1], border=1)
        pdf.cell(w=50, h=14, txt=columns[2], border=1)
        pdf.cell(w=50, h=14, txt=columns[3], border=1)
        pdf.cell(w=50, h=14, txt=columns[4], border=1, ln=1)

        #  Add rows
        for index, row in df.iterrows():
            pdf.set_font(family="Times", size=12, style="B")
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=50, h=10, txt=str(row[product_id]), border=1)
            pdf.set_font(family="Times", size=12)
            pdf.cell(w=70, h=10, txt=str(row[product_name]), border=1)
            pdf.cell(w=50, h=10, txt=str(row[amount_purchased]), border=1)
            pdf.cell(w=50, h=10, txt=str(row[price_per_unit]), border=1)
            pdf.cell(w=50, h=10, txt=str(row[total_price]), border=1, ln=1)

        # Add last row
        total_sum = df[total_price].sum()

        pdf.set_font(family="Times", size=12, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=50, h=10, txt="", border=1)
        pdf.cell(w=70, h=10, txt="", border=1)
        pdf.cell(w=50, h=10, txt="", border=1)
        pdf.cell(w=50, h=10, txt="", border=1)
        pdf.cell(w=50, h=10, txt=str(total_sum), border=1, ln=1)

        # Add footer
        pdf.ln(10)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Total : {total_sum} eur", ln=1)
        pdf.cell(w=35, h=10, txt=company_name)
        pdf.image(image_path, w=12)
        pdf.ln(5)
        pdf.set_font(family="Times", size=12)
        pdf.cell(w=50, h=8, txt="Thank you for shopping.", ln=1)
        pdf.cell(w=50, h=8, txt="Have a nice day! :)", ln=1)

        # Finish
        if not os.path.exists(pdfs_path):
            os.makedirs(pdfs_path)
        pdf.output(f"{pdfs_path}/{filename}.pdf")
