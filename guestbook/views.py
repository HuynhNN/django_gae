# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView
from google.appengine.api import users
from google.appengine.ext import ndb
from guestbook.models import *
from guestbook.forms import *
import logging as logger
import datetime

def force_int(value, default=0):
	try:
		return int(value)
	except Exception:
		return default

class Main_View(TemplateView):
	template_name = 'index.html'

	def get_infor_user(self):
		is_admin = False
		user_logined = users.get_current_user()
		url = users.create_login_url(self.request.get_full_path())
		url_linkText = 'Login'
		if user_logined:
			url = users.create_logout_url(self.request.get_full_path())
			url_linkText = 'Logout'
		if users.is_current_user_admin():
			is_admin = True
		return is_admin, user_logined, url, url_linkText

	def get(self, request, *args, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		if guestbook_name == '' or guestbook_name is None:
			return redirect('%s?guestbook_name=%s' % (reverse_lazy('guestbook:index'), DEFAULT_GUESTBOOK_NAME))
		return self.render_to_response(self.get_context_data(guestbook_name, **kwargs))

	def get_context_data(self, guestbook_name, **kwargs):
		limit = force_int(self.request.GET.get('limit', 3))
		cursor = self.request.GET.get('cursor', None)
		context = super(Main_View, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['greetings'], context['cursor_next'], context['more'] = Greeting.get_greeting(guestbook_name, limit, cursor)
		context['is_admin'], context['user_logined'], context['url'], context['url_linkText'] = self.get_infor_user()
		return context


class NewGreetingView(FormView):
	template_name = 'create_greeting.html'
	form_class = PostGreetingForm
	success_url = reverse_lazy('guestbook:index')

	def get(self, request, *args, **kwargs):
		guestbook_name = kwargs['pk']
		form = PostGreetingForm(initial={'guestbook_name': guestbook_name})
		return self.render_to_response(self.get_context_data(form=form))

	def form_valid(self, form):
		@ndb.transactional(xg=True)
		def txt():
			guestbook_name = form.cleaned_data.get('guestbook_name')
			content = form.cleaned_data.get('greeting_message')
			greeting = Greeting(parent=get_guestbook_key(guestbook_name))
			if users.get_current_user():
				greeting.author = users.get_current_user()
			greeting.content = content
			greeting.put()
			return guestbook_name
		guestbook_name = txt()
		url = self.success_url
		self.success_url = '%s?guestbook_name=%s' % (url, guestbook_name)
		return super(NewGreetingView, self).form_valid(form)

	def get_context_data(self, **kwargs):
		guestbook_name = kwargs['form']['guestbook_name'].value()
		form = kwargs['form']
		context = super(NewGreetingView, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['form'] = form
		return context


class DeleteGreetingView(TemplateView):

	def post(self, request, *args, **kwargs):
		greeting_id = kwargs['greeting_id']
		guestbook_name = kwargs['guestbook_name']
		self.delete(int(greeting_id), guestbook_name)
		return redirect('%s?guestbook_name=%s' % (reverse_lazy('guestbook:index'), guestbook_name))

	def delete(self, greeting_id, guestbook_name):
		greeting = Greeting.get_by_id(greeting_id, get_guestbook_key(guestbook_name))
		user = users.get_current_user()
		is_admin = users.is_current_user_admin()

		@ndb.transactional(xg=True)
		def txt():
			greeting.key.delete()
			return greeting.key

		if greeting:
			if is_admin or (user and greeting.author == user):
				key = txt()
				logger.info('Deleted %r', key)
			else:
				logger.warning('You can not delete.')
		else:
			logger.error('Greeting is not exist.')


class EditGreetingView(FormView):
	template_name = 'edit_greeting.html'
	form_class = EditGreetingForm
	success_url = reverse_lazy('guestbook:index')

	def get(self, request, *args, **kwargs):
		greeting_id = kwargs['greeting_id']
		guestbook_name = kwargs['guestbook_name']
		greeting = Greeting.get_by_id(int(greeting_id), get_guestbook_key(guestbook_name))
		if greeting is None:
			return
		form = EditGreetingForm(initial={
			'guestbook_name': guestbook_name,
			'greeting_message': greeting.content,
			'greeting_id': int(greeting_id)
		})
		return self.render_to_response(self.get_context_data(form=form))

	def form_valid(self, form):
		guestbook_name = form.cleaned_data.get('guestbook_name')
		self.update(form)
		url = self.success_url
		self.success_url = '%s?guestbook_name=%s' % (url, guestbook_name)
		return super(EditGreetingView, self).form_valid(form)

	def update(self, form):
		greeting = Greeting.get_by_id(int(form.cleaned_data.get('greeting_id')), get_guestbook_key(form.cleaned_data.get('guestbook_name')))
		user = users.get_current_user()
		is_admin = users.is_current_user_admin()

		@ndb.transactional(xg=True)
		def txt():
			greeting.content = form.cleaned_data.get('greeting_message')
			greeting.updated = datetime.datetime.now()
			greeting.user_updated = user
			greeting.put()
			return greeting.key

		if greeting:
			if is_admin or (user and greeting.author == user):
				key = txt()
				logger.info('Deleted %r', key)
			else:
				logger.warning('You can not delete.')
		else:
			logger.error('Greeting is not exist.')

	def get_context_data(self, **kwargs):
		guestbook_name = kwargs['form']['guestbook_name'].value()
		form = kwargs['form']
		context = super(EditGreetingView, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['form'] = form
		return context
