import pandas as pd
from pymongo import MongoClient


final_df = pd.read_csv("User_data.csv")

cgpa=list(final_df['CGPA'])
cgpa = [float(i) for i in cgpa]
final_df['CGPA'] = cgpa
# final_df.to_dict('records')


client = MongoClient('mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb', 27017)
db = client.sepcs
collection = db.user_data
collection.insert_many(final_df.to_dict('records'))