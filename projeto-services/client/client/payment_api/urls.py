from django.conf.urls import url

from .views import *

app_name ="payment"

urlpatterns = [
    url(r'^pix_payment$', pix_payment, name='pix_payment'),
    url(r'^get_bilings$', get_bilings, name='get_bilings'),
    url(r'^pix_revision$', pix_revision, name='pix_revision'),
]