from django.conf.urls import url
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r"^homepage", HomePage.as_view(), name="homepage"),
    url(r"^logout$", logout.as_view(), name='logout'),
    url(r"^update", updatePassword.as_view(), name="updatePassword"),
    url(r"^company", Company_list.as_view(), name="company_list"),
    url(r"^register", register.as_view(), name="register_company"),
    url(r"^uploadResume", uploadResume.as_view(), name="upload_resume"),
    url(r"^viewSchedule",viewSchedule.as_view(),name = "viewSched"),
    url(r"^blog$",Blog.as_view(),name = "blogView"),
    url(r"^blogdetails$",BlogDetails.as_view(),name="blogDetailsView")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
