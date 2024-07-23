from PyPDF2 import PdfReader
import pandas as pd
import requests
from urllib.parse import urlparse
import os
import re
import uuid

def clean_text(text):
    # Remove leading and trailing spaces from each line
    text = "\n".join(line.strip() for line in text.splitlines())

    # Replace multiple spaces between words with a single space
    text = re.sub(r"\s+", " ", text)

    # Remove extra empty lines
    text = re.sub(r"\n\s*\n", "\n", text)

    return text.strip()


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


def extract_and_save(pdf_file_name,uuid):
    # Read PDF content
    pdf_text = ""

    with open(pdf_file_name, "rb") as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            pdf_text += page.extract_text()
    pdf_text = clean_text(pdf_text)
    print('--------------------------------------------------------------------------------------------------------------------------------------------------')

    text_chunks = []
    string_start_index = 0
    string_end_index = 1024
    length_of_pdf_text = len(pdf_text)

    while string_end_index < length_of_pdf_text:
        while pdf_text[string_end_index] != ' ':
            if string_end_index <= string_start_index:
                text_chunks.append(pdf_text[string_start_index:string_start_index+1024])
                string_start_index += 1024
                string_end_index = string_start_index + 1024
                break
            string_end_index -= 1
        else:
            text_chunks.append(pdf_text[string_start_index:string_end_index])
            string_start_index = string_end_index
            string_end_index = string_start_index + 1024

    if string_start_index < length_of_pdf_text < string_end_index:
        text_chunks.append(pdf_text[string_end_index:])


    try:
        df = pd.read_csv('result.csv')
        new_df = pd.DataFrame.from_dict({
            'uuid' : [uuid] * len(text_chunks),
            'text_data': text_chunks
        })
        df = pd.concat([df,new_df],ignore_index=True)
        df.to_csv('result.csv',index=None)

    except:
        df = pd.DataFrame.from_dict({
            'uuid' : [uuid]*len(text_chunks),
            'text_data': text_chunks
        })
        df.to_csv('result.csv',index=None)




df = pd.read_excel("table.xlsx")

#create a uuids CSV for easier and faster lookup

uuids = [str(uuid.uuid4()) for _ in range(len(df["URL"]))]
uuids_df = pd.DataFrame.from_dict({
    'uuid' : uuids,
    'URL' : df["URL"]
})
uuids_df.set_index('uuid',inplace=True)
file_names = []
for index,url in enumerate(df["URL"]):
    file_name = download_pdf(url)
    file_names.append(file_name)
    extract_and_save(file_name,uuids[index])

uuids_df.insert(0,'file_name',file_names)
uuids_df.to_csv('uuid_url.csv')
