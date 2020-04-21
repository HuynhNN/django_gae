# -*- coding: utf-8 -*-

from django.http import HttpResponse
import json
import re


_RE_SNAKE_CASE = re.compile(r'[-_]')
_RE_CAMEL_CASE = re.compile(r'([a-z0-9])([A-Z])')


def _camelize_dict_keys(value):
	c, ck = camelize, _camelize_dict_keys
	if isinstance(value, dict):
		return value.__class__([(c(k), ck(v)) for k, v in value.items()])
	elif isinstance(value, (list, tuple)):
		return value.__class__([ck(v) for v in value])
	else:
		return value


def camelize(value):
	"""Convert snake_case string to lowerCamelCase"""
	parts = _RE_SNAKE_CASE.split(value)
	return ''.join(parts[:1] + [part.capitalize() for part in parts[1:]])


def snakify(value):
	"""Convert camelCase string to snake_case"""
	return _RE_CAMEL_CASE.sub(r'\1_\2', value).lower()


class JSONResponseMixin(object):

	response_class = HttpResponse

	def render_to_response(self, context, **response_kwargs):
		return self.render_to_json_response(context, **response_kwargs)

	def render_to_json_response(self, context, **response_kwargs):
		response_kwargs['content_type'] = 'application/json; charset=utf-8'
		return self.response_class(self.convert_context_to_json(context), **response_kwargs)

	def convert_context_to_json(self, context):
		return json.dumps(_camelize_dict_keys(context))
