from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r"^login$", login.as_view(), name="login"),
    url(r"^logout$", logout.as_view(), name='logout')
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
