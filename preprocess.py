#goal of this script is to take in pdfs and return text and doc name in a json format
#considering a folder is given full of docs

import pymupdf  
import os
from typing import TypedDict, NotRequired
import json 
import re

class DocFormat(TypedDict):
    name : str
    text : str
    #date : NotRequired[datetime]  


def extract_text_from_pdf(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    text = re.sub(r'\s+', ' ', text)
    return text


metadata : DocFormat = {}
working_dir = os.getcwd()
folder_path = ''
file_path = 'test.pdf'

if folder_path == '':
    full_path = working_dir + "/" + file_path

    text = extract_text_from_pdf(full_path)
    metadata["name"] = file_path
    metadata["text"] = text

else:

    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)

        text = extract_text_from_pdf(full_path)

        metadata["name"] = filename
        metadata["text"] = text
    

try:
    with open("metadata.json", "x", encoding="utf-8") as f:
        with open("metadata.json", "a", encoding="utf-8") as f:
            f.write(json.dumps(metadata, indent=4))
            print(f"File created at {os.getcwd()}/metadata.json")

except FileExistsError:
    print("file.txt already exists, exclusive creation aborted.")




#Features to add here:
#Add a regex date finder to find the date of this document 




