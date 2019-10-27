import pandas as pd
from pymongo import MongoClient

import random
import string

def randomString(stringLength):
    """Generate a random string with the combination of lowercase and uppercase letters """

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))
final_df = pd.read_csv("User_data.csv")

cgpa=list(final_df['cgpa'])
cgpa = [float(i) for i in cgpa]

final_df['cgpa'] = cgpa
# final_df.to_dict('records')
password = [randomString(8) for i in cgpa]
print(password[0])
final_df['password']= password
print(final_df.columns)
# client = MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb', 27017)
client = MongoClient('localhost', 27017)
db = client.sepcs
collection = db.user_data
collection.drop()
collection = db.user_data
collection.insert_many(final_df.to_dict('records'))