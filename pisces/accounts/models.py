from mongoengine import Document, fields
from datetime import datetime


# Create your models here.
class Company(Document):
    company = fields.StringField()
    postal_address = fields.StringField()
    about_the_company = fields.StringField()
    company_sector = fields.StringField()
    mode_of_selection = fields.ListField()
    interview_process = fields.StringField()
    job_description = fields.StringField()
    disciplines = fields.DictField()
    criteria = fields.DictField()
    position = fields.StringField
    location = fields.StringField()
    job_status = fields.ListField()
    compensation = fields.DictField()
    bond = fields.StringField()
    website = fields.StringField()
    registration_deadline = fields.DateTimeField(default=datetime.now, blank=True)
    test_date = fields.DateTimeField(default=datetime.now, blank=True)
    interview_date = fields.DateTimeField(default=datetime.now, blank=True)