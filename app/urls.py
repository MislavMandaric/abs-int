from django.conf.urls import patterns, include, url
import app

from .views import Index
urlpatterns = patterns('',
	 url(r'^', Index.as_view(), name="index"),
)
