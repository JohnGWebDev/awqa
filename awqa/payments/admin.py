from django.contrib import admin
from .models import Price, Product

# Register your models here.
admin.site.register(Product)
admin.site.register(Price)