# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from guestbook.views import *

app_name = 'guestbook'
urlpatterns = patterns('',
	url(r'^(?P<greeting_id>\d+)/(?P<guestbook_name>.*)/delete/$', DeleteGreetingView.as_view(), name='delete'),
	url(r'^(?P<greeting_id>\d+)/(?P<guestbook_name>.*)/edit/$', EditGreetingView.as_view(), name='edit'),
	url(r'^(?P<pk>.*)/new/$', NewGreetingView.as_view(), name='new'),
	url(r'^$', Main_View.as_view(), name='index'),
)
