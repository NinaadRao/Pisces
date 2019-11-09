from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^schedule$", DateView.as_view(), name="schedule"),
    url(r"^lab-list$", LabListView.as_view(), name="lab-list"),
    url(r"^booking$", BookView.as_view(), name="booking")
]
