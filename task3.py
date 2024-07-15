from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import csv
import pandas as pd
import requests
from urllib.parse import urlparse
import os
def download_pdf(url):
    response = requests.get(url)
    # Check if the request was successful
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    print(filename)
    if response.status_code == 200:
        # Open a file in binary-write mode
        with open(filename, "wb") as file:
            # Write the content of the response to the file
            file.write(response.content)
        print("PDF downloaded and saved successfully.")
        return file.name
    else:
        print(f"Failed to download PDF. Status code: {response.status_code}")
        return None


def extract_and_save(pdf_file_name):
    # Function to read PDF content
    def read_pdf(pdf_file_name):
        with open(pdf_file_name, 'rb') as file:
            reader = PdfReader(file)
            text = ''
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text

    # Path to the PDF file
    # file_path = '/home/technoidentity/Downloads/pdf2.pdf'

    # Read the PDF content
    pdf_text = read_pdf(pdf_file_name)

    # Initialize the text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=0,
    )

    # Split the PDF content into chunks
    split_text = splitter.create_documents([pdf_text])

    csv_file_name = pdf_file_name + '.csv'

    # write header rows in csv
    with open(csv_file_name,'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['text_data'])

    # Display the chunks
    for chunk in split_text:
        chunk.metadata['file'] = pdf_file_name
        text = chunk.page_content + ""
        # print(len(text))
        new_text = ''
        for line in text.split('\n'):
            # remove excess whitespace from beginning and end
            line = line.strip()
            #ignore empty lines
            if line:
                new_text += line
        with open(csv_file_name,'a',newline='') as file:
            writer = csv.writer(file)
            writer.writerow([new_text])

df = pd.read_excel('table.xlsx')

for url in df['URL']:
    file_name = download_pdf(url)
    extract_and_save(file_name)


