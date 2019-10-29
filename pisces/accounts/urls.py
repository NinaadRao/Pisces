from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^login$", login.as_view(), name="login"),
    url(r"^logout$", logout.as_view(), name='logout'),
    url(r"^update",updatePassword.as_view(),name="updatePassword"),
    url(r"^policy$",policy.as_view(),name="policy")
]
'''
urlpatterns = [
    url(r"^login/$", login_view, name = "login"),
]

urlpatterns += [
    url(r"^register/$", register_view, name = "register"),
]

urlpatterns += [
    url(r'^logout/$', logout_view, name = "logout"),
]'''
