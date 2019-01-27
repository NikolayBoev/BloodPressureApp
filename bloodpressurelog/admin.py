from django.contrib import admin
from . import models

class BloodPressureAdmin(admin.ModelAdmin):
    list_display = ("topNumber",  "bottomNumber")


admin.site.register(models.BloodPressure, BloodPressureAdmin)
