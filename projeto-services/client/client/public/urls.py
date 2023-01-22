from django.conf.urls import url
from .views import *

app_name="public"

urlpatterns = [
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^log_session$', log_session, name='log_session'),
]