# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView
from google.appengine.api import users
from google.appengine.ext import ndb
from guestbook.models import *
from guestbook.forms import *
import logging as logger


class Main_View(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		if guestbook_name == '' or guestbook_name is None:
			guestbook_name = DEFAULT_GUESTBOOK_NAME
		q = Greeting.query(ancestor=get_guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = q.fetch()
		user = users.get_current_user()
		if user:
			url = users.create_logout_url(self.request.get_full_path())
			url_linkText = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linkText = 'Login'
		if users.is_current_user_admin():
			admin = True
		else:
			admin = False
		context = super(Main_View, self).get_context_data(**kwargs)
		context['admin'] = admin
		context['user_logined'] = user
		context['greetings'] = greetings
		context['guestbook_name'] = guestbook_name
		context['url'] = url
		context['url_linkText'] = url_linkText
		return context


class Sign_View(FormView):
	template_name = 'sign.html'
	form_class = PostGreetingForm
	success_url = reverse_lazy('guestbook:index')

	def get(self, request, *args, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name')
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
		return super(Sign_View, self).form_valid(form)

	def get_context_data(self, **kwargs):
		guestbook_name = kwargs['form']['guestbook_name'].value()
		form = kwargs['form']
		context = super(Sign_View, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['form'] = form
		return context


class DeleteGreetingView(FormView):
	template_name = 'index.html'
	form_class = DeleteGreetingForm
	success_url = reverse_lazy('guestbook:index')

	def form_valid(self, form):
		greeting_id = form.cleaned_data.get('greeting_id')
		guestbook_name = form.cleaned_data.get('guestbook_name')
		self.delete(greeting_id, guestbook_name)
		url = self.success_url
		self.success_url = '%s?guestbook_name=%s' % (url, guestbook_name)
		return super(DeleteGreetingView, self).form_valid(form)

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
	template_name = 'edit.html'
	form_class = EditGreetingForm
	success_url = reverse_lazy('guestbook:index')

	def get(self, request, *args, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name')
		greeting_message = self.request.GET.get('greeting_message')
		greeting_id = self.request.GET.get('greeting_id')
		form = EditGreetingForm(initial={
			'guestbook_name': guestbook_name,
			'greeting_message': greeting_message,
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