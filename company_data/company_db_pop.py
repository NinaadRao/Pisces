import os
import json
from pymongo import MongoClient

path = 'Company_info'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(file)

client = MongoClient('localhost', 27017)
db = client.sepcs
collection_company = db.company_data

for f in files:
    with open('Company_info/' + f) as fi:
        company_data = json.load(fi)
    collection_company.insert_one(company_data)  

client.close()
