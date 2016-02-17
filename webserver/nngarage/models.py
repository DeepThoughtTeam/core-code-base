from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


# Create your models here.
class Profile(models.Model):
    # Password field
    password1 = models.CharField(max_length=100, default="", blank=True)
    # Confirm Password field
    password2 = models.CharField(max_length=100, default="", blank=True)
    first_name = models.CharField(max_length=30, default="", blank=True)
    last_name = models.CharField(max_length=30, default="", blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    image = models.ImageField(upload_to="profile-photos/%m/%d/%Y")


class NetDescription(models.Model):
    name = models.CharField(max_length=255, blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # For now, it is specified as JSON format
    file_ins = models.FileField(upload_to="net_description/file/%m/%d/%Y")
    # The screenshot for the neural network
    screenshot = models.ImageField(upload_to="net_description/image/%m/%d/%Y")
    dateTime = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_net_desc_meta(username):
        author = User.objects.get(username=username)
        nn_desc_meta = NetDescription.objects.filter(author=author).defer("file_ins")
        return nn_desc_meta








