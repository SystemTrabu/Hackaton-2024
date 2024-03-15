# api/urls.py
from django.urls import path
from .views import JSONUploadView

urlpatterns = [
    path('upload/', JSONUploadView.as_view(), name='json_upload'),
]
