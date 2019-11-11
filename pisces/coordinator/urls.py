from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r"^homepage", HomePage.as_view(), name="homepage"),
    url(r"^logout$", logout.as_view(), name='logout'),
    url(r"^company", Company_list.as_view(), name="company_list"),
    url(r"^schedule$", LabListView.as_view(), name="schedule"),
    url(r"^search$", Search.as_view(), name="search"),
]
