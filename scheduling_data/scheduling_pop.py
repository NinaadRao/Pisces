import os
import json
import pprint

from bson import ObjectId
from pymongo import MongoClient
import datetime

client = MongoClient('localhost', 27017)
db = client.sepcs
collection_company = db.company_data
collection_user = db.user_data
collection_lab = db.labs

schedules = []
lab_ids = [id for id in collection_lab.find().distinct("_id")]
student_ids = [id for id in collection_user.find().distinct("_id")]
for company in collection_company.find():
    dictionary = {"_id": company["_id"],
                  "student_list": student_ids,
                  "seating_information": {
                      "time": datetime.datetime.strptime("10:00:00", "%H:%M:%S"),
                      "labs": lab_ids
                  }}
    schedules.append(dictionary)

collection = db.scheduling_information
result = collection.insert_many(schedules)
print("Done")
