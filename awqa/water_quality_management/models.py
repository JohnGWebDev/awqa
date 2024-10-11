from django.conf import settings
from django.db import models
from django.urls import reverse

# Create your models here.

User = settings.AUTH_USER_MODEL

class Aquarium(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("aquarium-detail", kwargs={"pk": self.pk})
    

class FreshWaterParameterLogEntry(models.Model):
    aquarium = models.ForeignKey(Aquarium, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class PHChoices(models.TextChoices):
        SIX = "6.0", "6.0"
        SIXPOINTFOUR = "6.4", "6.4"
        SIXPOINTSIX = "6.6", "6.6"
        SIXPOINTEIGHT = "6.8", "6.8"
        SEVEN = "7.0", "7.0"
        SEVENPOINTTWO = "7.2", "7.2"
        SEVENPOINTSIX = "7.6", "7.6"
        NA = "N/A", "N/A"

    ph = models.CharField(
        max_length=3,
        choices=PHChoices.choices,
        default=PHChoices.SIX
    )

    class HighRangePHChoices(models.TextChoices):
        SEVENPOINTFOUR = "7.4", "7.4"
        SEVENPOINTEIGHT = "7.8", "7.8"
        EIGHT = "8.0", "8.0"
        EIGHTPOINTTWO = "8.2", "8.2"
        EIGHTPOINTFOUR = "8.4", "8.4"
        EIGHTPOINTEIGHT = "8.8", "8.8"
        NA = "N/A", "N/A"

    high_range_ph = models.CharField(
        max_length=3,
        choices=HighRangePHChoices.choices,
        default=HighRangePHChoices.SEVENPOINTFOUR
    )

    class AmmoniaChoices(models.TextChoices):
        ZERO = "0", "0"
        ZEROPOINTTWOFIVE = "0.25", "0.25"
        ZEROPOINTFIVE = "0.5", "0.5"
        ONE = "1.0", "1.0"
        TWO = "2.0", "2.0"
        FOUR = "4.0", "4.0"
        EIGHT = "8.0", "8.0"
        NA = "N/A", "N/A"

    ammonia = models.CharField(
        max_length=4,
        choices=AmmoniaChoices.choices,
        default=AmmoniaChoices.ZERO
    )
    
    class NitriteChoices(models.TextChoices):
        ZERO = "0", "0"
        ZEROPOINTTWOFIVE = "0.25", "0.25"
        ZEROPOINTFIVE = "0.5", "0.5"
        ONE = "1.0", "1.0"
        TWO = "2.0", "2.0"
        FIVE = "5.0", "5.0"
        NA = "N/A", "N/A"

    nitrite = models.CharField(
        max_length=4,
        choices=NitriteChoices.choices,
        default=NitriteChoices.ZERO
    )

    class NitrateChoices(models.TextChoices):
        ZERO = "0", "0"
        FIVE = "5.0", "5.0"
        TEN = "10", "10"
        TWENTY = "20", "20"
        FOURTY = "40", "40"
        EIGHTY = "80", "80"
        ONEHUNDREDSIXTY = "160", "160"
        NA = "N/A", "N/A"

    nitrate = models.CharField(
        max_length=3,
        choices=NitrateChoices.choices,
        default=NitrateChoices.ZERO
    )

    def get_absolute_url(self):
        return reverse("log-entry-detail", kwargs={"pk": self.pk})
