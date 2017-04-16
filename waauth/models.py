from django.db import models
from django.contrib.auth.models import User

class WAUser(models.Model):
    user = models.OneToOneField(User, related_name="wa_user", unique=True)
    name = models.CharField(max_length=63, db_index=True)
    # Contact Id in Wild Apricot
    wa_id = models.CharField(max_length=150, unique=True)
    access_token = models.CharField(max_length=150, blank=True, null=True)
    refresh_token = models.CharField(max_length=150, blank=True, null=True)
