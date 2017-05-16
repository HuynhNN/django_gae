# -*- coding: utf-8 -*-

from django import forms


class PostGreetingForm(forms.Form):
	guestbook_name = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'True'}), label="Guestbook Name")
	greeting_message = forms.CharField(widget=forms.Textarea, label="Message", max_length=200)


class DeleteGreetingForm(forms.Form):
	greeting_id = forms.IntegerField(initial=0)
	guestbook_name = forms.CharField()


class EditGreetingForm(forms.Form):
	guestbook_name = forms.CharField(widget=forms.HiddenInput, label='')
	greeting_id = forms.IntegerField(widget=forms.HiddenInput, label='')
	greeting_message = forms.CharField(widget=forms.Textarea, label="Message", max_length=200)
