from django.conf.urls import url

from .views import *

app_name ="payment"

urlpatterns = [
    url(r'^pix_payment$', pix_payment, name='pix_payment'),
]