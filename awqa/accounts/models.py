from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here.

class UserCore(AbstractUser):

    is_private = models.BooleanField(default=False)
    max_aquariums = models.IntegerField(default=3)

    def can_create_aquarium(self):
        if self.aquarium_set.count() < self.max_aquariums:
            return True
        return False

    def __str__(self):
        return self.username
    
    def get_absolute_url(self):
        return reverse("accounts:user-profile", kwargs={"pk": self.pk})
    