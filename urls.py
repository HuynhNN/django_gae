# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^', include('guestbook.urls', namespace='guestbook')),
)
