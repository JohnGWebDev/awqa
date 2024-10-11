from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class UserCore(AbstractUser):

    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("user-profile", kwargs={"pk": self.pk})
    