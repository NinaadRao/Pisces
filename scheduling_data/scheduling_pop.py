import os
import json
import pprint

from bson import ObjectId
from pymongo import MongoClient
import datetime
import random

client = MongoClient('localhost', 27017)
db = client.sepcs
collection_company = db.company_data
collection_user = db.user_data
collection_lab = db.labs

schedules = []
lab_ids = [id for id in collection_lab.find().distinct("_id")]
student_ids = [id for id in collection_user.find().distinct("_id")]
slots = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

for company in collection_company.find():
    slot = random.choice(slots)
    dictionary = {"_id": company["_id"],
                  "student_list": student_ids,
                  "seating_information": {
                      "time": [slot],
                      "labs": lab_ids
                  }}
    schedules.append(dictionary)

collection = db.scheduling_information
result = collection.insert_many(schedules)
print("Done")
