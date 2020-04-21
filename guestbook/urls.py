from django.conf.urls import url
from .views import Index
from .api.api_view import Auth

urlpatterns = (
	url(r'^api/auth', Auth.as_view()),
	url(r'^', Index.as_view())
)
