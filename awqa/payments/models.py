from django.db import models

# Create your models here.


class Price(models.Model):
    title = models.CharField(max_length=50)
    price_id = models.CharField(max_length=50)

    def __str__(self):
        return self.title
    

class Product(models.Model):
    price = models.ForeignKey(Price, on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=250)