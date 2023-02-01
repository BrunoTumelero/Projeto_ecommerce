from django.conf.urls import url

from .views import *

app_name ="consumer"

urlpatterns = [
    url(r'^create_user$', create_user, name='create_user'),
    url(r'^add_card$', add_card, name='add_card'),
    url(r'^get_consumer_product$', get_consumer_product, name='get_consumer_product'),
    url(r'^search_product$', search_product, name='search_product'),
    url(r'^add_whishes_list$', add_whishes_list, name='add_whishes_list'),

    url(r'^test$', test, name='test'),
]