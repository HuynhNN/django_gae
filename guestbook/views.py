# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, FormView
from django import forms
from google.appengine.api import users
from guestbook.models import DEFAULT_GUESTBOOK_NAME, Greeting, get_guestbook_key


class Main_View(TemplateView):
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name', DEFAULT_GUESTBOOK_NAME)
		if guestbook_name == '' or guestbook_name is None:
			guestbook_name = DEFAULT_GUESTBOOK_NAME
		q = Greeting.query(ancestor=get_guestbook_key(guestbook_name)).order(-Greeting.date)
		greetings = q.fetch()
		if users.get_current_user():
			url = users.create_logout_url(self.request.get_full_path())
			url_linkText = 'Logout'
		else:
			url = users.create_login_url(self.request.get_full_path())
			url_linkText = 'Login'
		context = super(Main_View, self).get_context_data(**kwargs)
		context['greetings'] = greetings
		context['guestbook_name'] = guestbook_name
		context['url'] = url
		context['url_linkText'] = url_linkText
		return context


class Sign_Form(forms.Form):
	guestbook_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}),
									label='Guestbook name')
	greeting_message = forms.CharField(widget=forms.Textarea ,label='Message', max_length=200)


class Sign_View(FormView):
	template_name = 'sign.html'
	form_class = Sign_Form
	success_url = reverse_lazy('guestbook:index')

	def get(self, request, *args, **kwargs):
		guestbook_name = self.request.GET.get('guestbook_name')
		form = Sign_Form(initial={'guestbook_name': guestbook_name})
		return self.render_to_response(self.get_context_data(form=form))

	def form_valid(self, form):
		guestbook_name = form.cleaned_data.get('guestbook_name')
		content = form.cleaned_data.get('greeting_message')
		greeting = Greeting(parent=get_guestbook_key(guestbook_name))
		if users.get_current_user():
			greeting.author = users.get_current_user()
		greeting.content = content
		greeting.put()
		url = self.success_url
		self.success_url = '%s?guestbook_name=%s' % (url, guestbook_name)
		return super(Sign_View, self).form_valid(form)

	def form_invalid(self, form):
		return self.render_to_response(self.get_context_data(form=form))

	def get_context_data(self, **kwargs):
		guestbook_name = kwargs['form']['guestbook_name'].value()
		form = kwargs['form']
		context = super(Sign_View, self).get_context_data(**kwargs)
		context['guestbook_name'] = guestbook_name
		context['form'] = form
		return context
