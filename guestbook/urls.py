# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from guestbook.views import Main_View, Sign_View

app_name = 'guestbook'
urlpatterns = patterns('',
	url(r'^sign/$', Sign_View.as_view(), name='sign'),
	url(r'^$', Main_View.as_view(), name='index'),
)
