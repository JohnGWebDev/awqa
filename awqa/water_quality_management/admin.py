from django.contrib import admin
from .models import Aquarium, FreshWaterParameterLogEntry

# Register your models here.

class FreshwaterParameterLogEntryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Aquarium)
admin.site.register(FreshWaterParameterLogEntry, FreshwaterParameterLogEntryAdmin)