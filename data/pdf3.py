# -*- coding: utf-8 -*-
"""PDF2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Wpad_-11_-pv7ELNWtYCVM96mUQGns1k

# Importing OS
"""

import os

"""# Mounting the drive"""

# from google.colab import drive
# drive.mount('/content/drive')

"""# Installing and importing the libraries"""


# Run the code below on terminal
#pip install langchain pymupdf

"""# Text extraction from the PDF"""

import fitz  # PyMuPDF

def get_column_boxes(page, num_columns=2, margin=12):
    """
    Get bounding boxes for each column in a multi-column page.

    :param page: PyMuPDF page object.
    :param num_columns: Number of columns in the page.
    :param margin: Margin between columns.
    :return: List of bounding boxes for each column.
    """
    # Get the dimensions of the page
    page_width = page.rect.width
    page_height = page.rect.height

    # Calculate the width of each column
    column_width = (page_width - (margin * (num_columns - 1))) / num_columns

    # Create bounding boxes for each column
    column_boxes = []
    for i in range(num_columns):
        x0 = i * (column_width + margin)
        x1 = x0 + column_width
        rect = fitz.Rect(x0, 0, x1, page_height)
        column_boxes.append(rect)

    return column_boxes

def extract_text_from_columns(pdf_path, start_page, end_page, output_txt_path, num_columns=2, margin=10):
    """
    Extract text from a multi-column PDF and save to a .txt file.

    :param pdf_path: Path to the PDF file.
    :param start_page: Starting page number (0-indexed).
    :param end_page: Ending page number (0-indexed).
    :param output_txt_path: Path to the output .txt file.
    :param num_columns: Number of columns in the PDF.
    :param margin: Margin between columns.
    """
    # Open the PDF document
    doc = fitz.open(pdf_path)

    # Open a file to write the extracted text
    with open(output_txt_path, 'w') as f:
        # Loop through the specified range of pages
        for page_num in range(start_page, end_page + 1):
            page = doc[page_num]

            # Get bounding boxes for each column
            column_boxes = get_column_boxes(page, num_columns, margin)

            # Extract and write text from each column
            for rect in column_boxes:
                text = page.get_text("text", clip=rect)
                f.write(text)
                f.write("\n")
                f.write("-" * 80)
                f.write("\n")

    print(f"Text extracted from pages {start_page} to {end_page} and saved to {output_txt_path}")

# Defined variables
pdf_path = "/content/drive/My Drive/European Pharmacopoeia 8.0.pdf"
output_txt_path = "/content/drive/My Drive/Pharmacopoeia_reference.txt"
start_page = 3463  # Starting page number (0-indexed)
end_page = 3495   # Ending page number (0-indexed)

extract_text_from_columns(pdf_path, start_page, end_page, output_txt_path)

"""# Prettifying extracted text"""

def prettify_text(input_txt_path, output_txt_path):
    with open(input_txt_path, 'r') as file:
        text = file.read()

    # Remove unwanted line breaks and extra spaces
    lines = text.splitlines()
    pretty_lines = []

    for line in lines:
        # Strip leading and trailing whitespaces
        line = line.strip()

        # Skip empty lines
        if line:
            pretty_lines.append(line)

    # Join lines with a single newline
    pretty_text = "\n".join(pretty_lines)

    # Write prettified text to the output file
    with open(output_txt_path, 'w') as file:
        file.write(pretty_text)

# Defined variables
input_txt_path = "/content/drive/My Drive/Pharmacopoeia_reference.txt"
output_txt_path = "/content/drive/My Drive/Pharmacopoeia_prettifiedreference.txt"

prettify_text(input_txt_path, output_txt_path)