from django.db import models
from django.contrib.auth.models import User


class InfluencerProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, null=True)
    ig_link = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
