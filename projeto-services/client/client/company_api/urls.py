from django.conf.urls import url

from .views import *

app_name = "company"

urlpatterns = [
    url(r'^create_company$', create_company, name='create_company'),
    url(r'^create_new_product$', create_new_product, name='create_new_product'),
    url(r'^edit_product/(?P<pk>\d+)$', edit_product, name='edit_product'),
    url(r'^create_employee$', create_employee, name='create_employee'),
]