from django.conf.urls import url

from .views import *

app_name = "company"

urlpatterns = [
    url(r'^create_company$', create_company, name='create_company'),
    url(r'^create_specialty$', create_specialty, name='create_specialty'),
]