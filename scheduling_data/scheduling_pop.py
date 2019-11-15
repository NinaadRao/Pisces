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

lines = open("labs.txt").readlines()
global_lab_numbers = [line.split()[0] for line in lines]
schedules = []
labs_numbers = []
student_ids = [id for id in collection_user.find().distinct("_id")]
slots = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

for company in collection_company.find():
    slot = random.choice(slots)
    dictionary = {"_id": company["_id"],
                  "student_list": random.sample(student_ids, 100),
                  "seating_information": {
                      "time": [slot for i in range(10)],
                      "labs": random.sample(global_lab_numbers, 10)
                  }}
    schedules.append(dictionary)

collection = db.scheduling_information
result = collection.insert_many(schedules)
print("Done")
