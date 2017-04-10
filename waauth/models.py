from django.db import models
from django.contrib.auth.models import User

class WAUser(models.Model):
    user = models.OneToOneField(User, unique=True)
    name = models.CharField(max_length=63, db_index=True)
    wa_id = models.CharField(max_length=150, unique=True)
    access_token = models.CharField(max_length=150, blank=True, null=True)
    refresh_token = models.CharField(max_length=150, blank=True, null=True)
