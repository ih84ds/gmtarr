# Django
from django.conf.urls import url

# Custom
from waauth.views import authenticate_view, logout_view, register_view, test_view

urlpatterns = [
    url(r'^authenticate/?$', view=authenticate_view, name='authenticate'),
    url(r'^logout/?$', view=logout_view, name='logout'),
    url(r'^register/?$', view=register_view, name='register'),
    url(r'^test/?$', view=test_view, name='test'),
]