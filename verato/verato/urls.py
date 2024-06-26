"""
URL configuration for verato project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""
from django.contrib import admin
from django.urls import path, include

from ApiRest.views import JSONUploadView
from ApiRest.views import TextUploadView
from ApiRest.views import Generate
from ApiRest.views import createtxt



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/upload/', JSONUploadView.as_view(), name='json_upload'),
    path('api/up/', TextUploadView.as_view(), name='text_upload'),
    path('api/generate/', Generate.as_view(), name='generate'),
    path('api/download/',createtxt.as_view(), name='txt'),
]
