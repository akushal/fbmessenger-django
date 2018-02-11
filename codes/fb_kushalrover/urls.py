from django.conf.urls import  url, include
from .views import KushalRoverView
urlpatterns = [
	url(r'^webhooks/?$', KushalRoverView.as_view()) 
]
