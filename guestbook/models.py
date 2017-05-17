# -*- coding: utf-8 -*-

from google.appengine.datastore.datastore_query import Cursor
from google.appengine.ext import ndb

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'

def get_guestbook_key(guestbook_name = DEFAULT_GUESTBOOK_NAME):
	return ndb.Key('Guestbook', guestbook_name)


class Greeting(ndb.Model):
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)
	user_updated = ndb.UserProperty(default=None)
	updated = ndb.DateTimeProperty(auto_now_add=True)

	@classmethod
	def get_greeting(cls, guestbook_name, limit=3, cursor=None):
		cursor = Cursor(urlsafe=cursor)
		greetings, next_cursor, more = Greeting.query(ancestor=get_guestbook_key(guestbook_name)).\
			fetch_page(limit, start_cursor=cursor)
		cursor_next = None
		if next_cursor is not None:
			cursor_next = next_cursor.urlsafe()
		return greetings, cursor_next, more

