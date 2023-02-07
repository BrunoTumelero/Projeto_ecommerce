from django.conf.urls import url
from .views import *

app_name="public"

urlpatterns = [
    url(r'^login$', login, name='login'),
    url(r'^logout$', logout, name='logout'),
    url(r'^log_session$', log_session, name='log_session'),
    url(r'^get_products$', get_products, name='get_products'),
    url(r'^get_products_category$', get_products_category, name='get_products_category'),
]