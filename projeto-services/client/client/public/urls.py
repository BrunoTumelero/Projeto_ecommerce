from django.conf.urls import url
from .views import *

app_name="public"

urlpatterns = [
    url(r'^login$', login, name='login'),
    url(r'^create_state$', create_state, name='create_state'),
    url(r'^create_city$', create_city, name='create_city'),
]