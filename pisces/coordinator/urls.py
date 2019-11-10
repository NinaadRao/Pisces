from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^schedule$", LabListView.as_view(), name="schedule"),
    url(r"^list_labs$", ListLabs.as_view(), name="list_labs"),
    url(r"^upsert_booking$", UpsertBooking.as_view(), name="upsert_booking"),
    url(r"^remove_booking$", RemoveBooking.as_view(), name="remove_booking")
]
