#goal of this script is to take in pdfs and return text and doc name in a json format
#considering a folder is given full of docs

import pymupdf  
import os
from typing import TypedDict, NotRequired

class DocFormat(TypedDict):
    name : str
    text : str
    #date : NotRequired[datetime]  


def extract_text_from_pdf(file_path):
    doc = pymupdf.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    return text


metadata : DocFormat = {}
working_dir = os.getcwd()
folder_path = ''
file_path = 'gs_cover_letter_latest-2.pdf'

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
    

print(metadata)




