from django.conf.urls import url

from .views import *

app_name ="payment"

urlpatterns = [
    url(r'^pix_payment$', pix_payment, name='pix_payment'),
    url(r'^get_pix_bilings$', get_pix_bilings, name='get_pix_bilings'),
    url(r'^pix_revision$', pix_revision, name='pix_revision'),
    url(r'^generate_qr_code$', generate_qr_code, name='generate_qr_code'),
    url(r'^create_signature$', create_signature, name='create_signature'),
    url(r'^plan_subscribe$', plan_subscribe, name='plan_subscribe'),
]