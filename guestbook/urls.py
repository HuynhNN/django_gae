# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from guestbook.views import Main_View, Sign_View, DeleteGreetingView, EditGreetingView

app_name = 'guestbook'
urlpatterns = patterns('',
	url(r'^delete/$', DeleteGreetingView.as_view(), name='delete'),
	url(r'^edit/$', EditGreetingView.as_view(), name='edit'),
	url(r'^sign/$', Sign_View.as_view(), name='sign'),
	url(r'^$', Main_View.as_view(), name='index'),
)
