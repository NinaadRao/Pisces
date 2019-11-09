from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^schedule$", LabListView.as_view(), name="schedule")

]
