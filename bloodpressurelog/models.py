from django.db import models

from django.utils import timezone

class BloodPressure(models.Model): #GroceryList able name that inherits models.Model
    topNumber = models.IntegerField(default=120) # a varchar
    bottomNumber = models.IntegerField(default=80) # a IntegerField
    puls = models.IntegerField(default=80) # a text field 
    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date

    class Meta:
        ordering = ["-created"] #ordering by the created field

    def __int__(self):
        return self.id #name to be shown when called