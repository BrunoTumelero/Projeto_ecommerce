from django.conf.urls import url

from .views import *

app_name="adm"

urlpatterns = [
    url(r'^create_state$', create_state, name='create_state'),
    url(r'^create_city$', create_city, name='create_city'),
    url(r'^user_permission$', user_permission, name='user_permission'),
]