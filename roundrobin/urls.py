"""roundrobin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.conf.urls import include, url
from django.contrib import admin
import api.views

# This allows us to ensure we are already logged in via waauth
# before hitting the admin login page.
admin.site.login = login_required(admin.site.login)

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^waauth/', include('waauth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', api.views.index),
]
