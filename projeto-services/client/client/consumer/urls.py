from django.conf.urls import url

from .views import *

app_name ="consumer"

urlpatterns = [
    url(r'^create_user$', create_user, name='create_user'),
    url(r'^add_card$', add_card, name='add_card'),
    url(r'^get_consumer_product$', get_consumer_product, name='get_consumer_product'),

    url(r'^test$', test, name='test'),
]