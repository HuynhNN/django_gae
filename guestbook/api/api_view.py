from django.views.generic import FormView
from google.appengine.api import users
from guestbook.api import JsonResponse


class Auth(JsonResponse.JSONResponseMixin, FormView):

	def get(self, request, *args, **kwargs):
		if users.get_current_user():
			url = users.create_logout_url('/')
			url_linktext = 'Logout'
			user_email = users.get_current_user().email()
		else:
			url = users.create_login_url('/')
			url_linktext = 'Login'
			user_email = ''

		context = {
			'url': url,
			'url_linktext': url_linktext,
			'user_email': user_email
		}
		return self.render_to_response(context)
