from django.conf.urls import url
from .views import *

app_name="public"

urlpatterns = [
    url(r'^login$', login, name='login'),
]