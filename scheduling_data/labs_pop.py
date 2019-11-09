from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.sepcs

file = open("labs.txt", 'r')
lines = file.readlines()

room_dicts = []
room_no = [line.replace("\n", "").split(" ")[0] for line in lines]
capacities = [line.replace("\n", "").split(" ")[1] for line in lines]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
time_slots = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

day_info = []
for day in days:
    free_slots = []
    for time_slot in time_slots:
        free_slots.append({"time_slot": time_slot, "free_labs": room_no})
    day_info.append({"Day": day, "free_slots": free_slots})

# print(day_info)

collection = db.labs
result = collection.insert_many(day_info)
# print(day_info[0])
