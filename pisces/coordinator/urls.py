from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r"^homepage", HomePage.as_view(), name="homepage"),
    url(r"^logout$", logout.as_view(), name='logout'),
    url(r"^company", Company_list.as_view(), name="company_list"),
    url(r"^schedule$", LabListView.as_view(), name="schedule"),
    url(r"^search$", Search.as_view(), name="search"),
    url(r"^search_results$", SearchResults.as_view(), name="search_results"),
    url(r"^list_labs$", ListLabs.as_view(), name="list_labs"),
    url(r"^get_booking$", DisplayBooking.as_view(), name="get_booking"),
    url(r"^upsert_booking$", UpsertBooking.as_view(), name="upsert_booking"),
    url(r"^remove_booking$", RemoveBooking.as_view(), name="remove_booking"),
    url(r"^automail", Automail.as_view(), name="automail"),
    url(r"^remove_booking$", RemoveBooking.as_view(), name="remove_booking"),
    url(r"^registered_success$", RegistrationSuccessfulView.as_view(), name="registered_successfully"),
    url(r"^uploadCompanyInfo$", UploadCompanyInfo.as_view(), name="uploadCompanyInfo"),
]
