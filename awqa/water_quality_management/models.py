from django.conf import settings
from django.db import models
from . import choices
from django.urls import reverse

# Create your models here.

User = settings.AUTH_USER_MODEL

class Aquarium(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=35)
    description = models.TextField(max_length=250, blank=True, default='')
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("water_quality_management:aquarium-detail", kwargs={"pk": self.pk})
    

class FreshWaterParameterLogEntry(models.Model):
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(max_length=250, blank=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    ph = models.CharField(max_length=3, choices=choices.PHChoices.choices, default=choices.PHChoices.SIX)
    high_range_ph = models.CharField(max_length=3, choices=choices.HighRangePHChoices.choices, default=choices.HighRangePHChoices.SEVENPOINTFOUR )
    ammonia = models.CharField(max_length=4, choices=choices.AmmoniaChoices.choices, default=choices.AmmoniaChoices.ZERO)
    nitrite = models.CharField(max_length=4, choices=choices.NitriteChoices.choices, default=choices.NitriteChoices.ZERO)
    nitrate = models.CharField(max_length=3, choices=choices.NitrateChoices.choices, default=choices.NitrateChoices.ZERO)

    def get_absolute_url(self):
        return reverse("water_quality_management:log-entry-detail", kwargs={"pk": self.pk})
