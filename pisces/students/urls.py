from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^homepage",HomePage.as_view(),name="homepage"),
    url(r"^logout$", logout.as_view(), name='logout'),
    url(r"^update",updatePassword.as_view(),name="updatePassword"),
    url(r"^company",Company_list.as_view(),name="company_list")

]
