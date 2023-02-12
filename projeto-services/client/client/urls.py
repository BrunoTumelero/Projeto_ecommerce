from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings

from client.public_api import urls as public_urls
from client.consumer_api import urls as consumer_urls
from client.company_api import urls as company_urls
from client.adm_api import urls as adm_urls
from client.payment_api import urls as payment_urls

urlpatterns = [
    url(r'^public/', include(public_urls, namespace='public')),
    url(r'^consumer/', include(consumer_urls, namespace='consumer')),
    url(r'^company/', include(company_urls, namespace='company')),
    url(r'^adm/', include(adm_urls, namespace='adm')),
    url(r'^payment/', include(payment_urls, namespace='payment')),
]
