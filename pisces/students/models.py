from django.db import models

# Create your models here.
from mongoengine import DynamicDocument, Document, fields
from datetime import datetime


# Create your models here.
class Company(DynamicDocument):
    meta = {'collection': 'company_data'}
    # company = fields.StringField()
    # postal_address = fields.StringField()
    # about_the_company = fields.StringField()
    # company_sector = fields.StringField()
    # mode_of_selection = fields.ListField()
    # interview_process = fields.StringField()
    # job_description = fields.StringField()
    # disciplines = fields.DictField()
    # criteria = fields.DictField()
    # position = fields.StringField
    # location = fields.StringField()
    # job_status = fields.ListField()
    # compensation = fields.DictField()
    # bond = fields.StringField()
    # website = fields.StringField()
    # registration_deadline = fields.DateTimeField(default=datetime.now, blank=True)
    # test_date = fields.DateTimeField(default=datetime.now, blank=True)
    # interview_date = fields.DateTimeField(default=datetime.now, blank=True)


class User(DynamicDocument):
    meta = {'collection': 'user_data'}
    # name = fields.StringField()
    # srn = fields.StringField()
    # gender = fields.StringField()
    # cgpa = fields.StringField()
    # tenth = fields.FloatField()
    # twelfth = fields.FloatField()
    # year_of_pass = fields.IntField()
    # highest_qualification = fields.StringField()
    # college = fields.StringField()
    # department = fields.StringField()
    # password = fields.StringField()


class scheduling_information(DynamicDocument):
    meta = {'collection': 'scheduling_information'}


class labs(DynamicDocument):
    meta = {'collection':'labs'}

class blogging(DynamicDocument):
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    meta = {'collection':'blog'}
    created_on = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_on']


class CompanyInfo(DynamicDocument):
    meta = {'collection': 'company_wiki_info'}
