from django.db import models
from django.contrib.auth.models import User


class UserPersonalData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profile_picture_drive_url = models.CharField(max_length=255, null=True, blank=True)
    wallet_security_stamp = models.CharField(max_length=255, null=True, blank=True)
