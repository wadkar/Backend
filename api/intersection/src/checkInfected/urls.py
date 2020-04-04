from django.conf.urls import include, url
from .import views

from rest_framework import routers


urlpatterns = [
    url(r'^', views.main, name='index')
]
