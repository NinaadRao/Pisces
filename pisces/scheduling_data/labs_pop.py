from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.sepcs

file = open("labs.txt", 'r')
lines = file.readlines()

room_dicts = []

for line in lines:
    splits = line.replace("\n", "").split(" ")
    dictionary = {'room_no': splits[0], "capacity": int(splits[1])}
    room_dicts.append(dictionary)

collection = db.labs
result = collection.insert_many(room_dicts)





