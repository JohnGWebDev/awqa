from django.db import models


class PHChoices(models.TextChoices):
    NA = "N/A", "N/A"
    SIX = "6.0", "6.0"
    SIXPOINTFOUR = "6.4", "6.4"
    SIXPOINTSIX = "6.6", "6.6"
    SIXPOINTEIGHT = "6.8", "6.8"
    SEVEN = "7.0", "7.0"
    SEVENPOINTTWO = "7.2", "7.2"
    SEVENPOINTSIX = "7.6", "7.6"


class HighRangePHChoices(models.TextChoices):
    NA = "N/A", "N/A"
    SEVENPOINTFOUR = "7.4", "7.4"
    SEVENPOINTEIGHT = "7.8", "7.8"
    EIGHT = "8.0", "8.0"
    EIGHTPOINTTWO = "8.2", "8.2"
    EIGHTPOINTFOUR = "8.4", "8.4"
    EIGHTPOINTEIGHT = "8.8", "8.8"


class AmmoniaChoices(models.TextChoices):
    NA = "N/A", "N/A"
    ZERO = "0", "0"
    ZEROPOINTTWOFIVE = "0.25", "0.25"
    ZEROPOINTFIVE = "0.5", "0.5"
    ONE = "1.0", "1.0"
    TWO = "2.0", "2.0"
    FOUR = "4.0", "4.0"
    EIGHT = "8.0", "8.0"


class NitriteChoices(models.TextChoices):
    NA = "N/A", "N/A"
    ZERO = "0", "0"
    ZEROPOINTTWOFIVE = "0.25", "0.25"
    ZEROPOINTFIVE = "0.5", "0.5"
    ONE = "1.0", "1.0"
    TWO = "2.0", "2.0"
    FIVE = "5.0", "5.0"


class NitrateChoices(models.TextChoices):
    NA = "N/A", "N/A"
    ZERO = "0", "0"
    FIVE = "5.0", "5.0"
    TEN = "10", "10"
    TWENTY = "20", "20"
    FOURTY = "40", "40"
    EIGHTY = "80", "80"
    ONEHUNDREDSIXTY = "160", "160"

