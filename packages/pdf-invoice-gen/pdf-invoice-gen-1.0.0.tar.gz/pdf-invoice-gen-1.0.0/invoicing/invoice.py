import os

import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

def generate(invoicesPath, pdfsPath, imagePath,
             product_id, product_name, amount_purchased,
             price_per_unit, total_price):
    """
    This function converts invoice Excel files into PDF

    :param invoicesPath: File Path where the invoice files are
    :type invoicesPath: str
    :param pdfsPath: File Path where the PDF outputs will be generated
    :type pdfsPath: str
    :param imagePath: Image Path for your company logo that will be embedded on the PDF generation
    :type imagePath: str
    :param product_id: id column of your invoice xlsx file
    :type product_id: str
    :param product_name: column name of the items to be invoiced
    :type product_name: str
    :param amount_purchased: column of the amount of purchased items
    :type amount_purchased: str
    :param price_per_unit: price per item
    :type price_per_unit: str
    :param total_price: total price paid for the items
    :type total_price: str
    :return: outputs PDF invoice files
    :rtype:
    """

    filepaths = glob.glob(f"{invoicesPath}/*.xlsx")

    # Read the files into a dataframe
    for file in filepaths:
        # Set a pdf document
        pdf = FPDF(orientation="P", unit="mm", format="A4")

        # Add page to the pdf document
        pdf.add_page()

        # Extract the filename  from the file and the Invoice Number and Date using split method on filename
        fileName = Path(file).stem
        invoice_nr, date = fileName.split("-")

        # Set the font
        pdf.set_font(family="Times", size=16, style="B")
        # Define the cells for the Invoice layout
        pdf.cell(w=50, h=10, txt=f"Invoice Nr: {invoice_nr}", ln=1)

        pdf.set_font(family="Times", size=12)
        pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)

        df = pd.read_excel(file, sheet_name="Sheet 1", engine="openpyxl")

        # Add Column Headers
        columns = list(df.columns)
        columns = [item.replace("_"," ").title() for item in columns]
        pdf.set_font(family="Times", size=10, style="B")
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=10, txt=columns[0], border=1)
        pdf.cell(w=50, h=10, txt=columns[1], border=1)
        pdf.cell(w=40, h=10, txt=columns[2], border=1)
        pdf.cell(w=30, h=10, txt=columns[3], border=1)
        pdf.cell(w=30, h=10, txt=columns[4], border=1, ln=1)

        # iterrate over the rows of the dataframe
        for idx, row in df.iterrows():
            pdf.set_font(family="Times", size=10)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(w=30, h=10, txt=str(row[product_id]), border=1)
            pdf.cell(w=50, h=10, txt=str(row[product_name]), border=1)
            pdf.cell(w=40, h=10, txt=str(row[amount_purchased]), border=1, align="C")
            pdf.cell(w=30, h=10, txt=str(row[price_per_unit]), border=1, align="C")
            pdf.cell(w=30, h=10, txt=str(row[total_price]), border=1, align="C", ln=1)

        # Add new cell row for the sum of total_price
        total_sum = df[total_price].sum()

        # Add total_sum to the PDF output
        pdf.set_font(family="Times", size=10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(w=30, h=10, txt="", border=1)
        pdf.cell(w=50, h=10, txt="", border=1)
        pdf.cell(w=40, h=10, txt="", border=1, align="C")
        pdf.cell(w=30, h=10, txt="", border=1, align="C")
        pdf.cell(w=30, h=10, txt=str(total_sum), border=1, align="C", ln=1)

        # Add new cell for Total price
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=30, h=10, txt=f"The total price is: {total_sum}", ln=1)

        # Add new cell for image
        pdf.set_font(family="Times", size=12, style="B")
        pdf.cell(w=25, h=10, txt="PythonHow")
        pdf.image(f"{imagePath}", w=8, h=8)


        # Save output to PDF
        if not os.path.exists(pdfsPath):
            os.makedirs(pdfsPath)
        pdf.output(f"{pdfsPath}/{fileName}.pdf")
