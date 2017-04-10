from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(redirect_field_name="redirect_uri")
def index(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)
