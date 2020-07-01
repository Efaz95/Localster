from django.db import models
from django.contrib.auth.models import User


class InfluencerProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=200, null=True, default="Go to settings to update")
    ig_link = models.CharField(max_length=200, null=True, default="Go to setting to update")
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip_code = models.IntegerField(null=True)
    followers = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class BusinessProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=200, null=True)
    street_address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zip_code = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Messages(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    msg_content = models.TextField(max_length=200, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


class Hire(models.Model):
    hired_by = models.ForeignKey(User, related_name="business", on_delete=models.CASCADE)
    hired_influencer = models.ForeignKey(User, related_name="influencer", on_delete=models.CASCADE)
