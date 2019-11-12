"""pisces URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .settings import *
urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [

    url(r'^accounts/', include(("accounts.urls", "accounts"), namespace="accounts")),
    url(r'^students/', include(("students.urls", "accounts"), namespace="students")),
    url(r'^coordinator/', include(("coordinator.urls", "accounts"), namespace="coordinator")),

]
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# print('This is the static root',settingsSTATIC_ROOT)
from django.conf import settings

urlpatterns += staticfiles_urlpatterns()
print('hello',settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATIC_ROOT)