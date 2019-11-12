from django.db import models
from mongoengine import DynamicDocument


# Create your models here.

class Company(DynamicDocument):
    meta = {'collection': 'company_data'}


class User(DynamicDocument):
    meta = {'collection': 'user_data'}


class Scheduling(DynamicDocument):
    meta = {'collection': 'scheduling_information'}


class Labs(DynamicDocument):
    meta = {'collection': 'labs'}
