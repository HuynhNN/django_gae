# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

def get_guestbook_key(guestbook_name = DEFAULT_GUESTBOOK_NAME):
	return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
