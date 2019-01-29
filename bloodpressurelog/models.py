from django.db import models
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
# I also get the error if I define the validator here
def validate_name(value):
	if value == '':
		raise ValidationError(u'%s cannot be left blank' % value)
		
class BloodPressure(models.Model): #BloodPressure able name that inherits models.Model
	topNumber = models.IntegerField(default=120, validators=[validate_name]) # a IntegerField
	bottomNumber = models.IntegerField(default=80) # a IntegerField
	puls = models.IntegerField(default=80) # a IntegerField
	created = models.DateField(default=timezone.now().strftime("%Y-%m-%d")) # a date

	class Meta:
		ordering = ["-created"] #ordering by the created field

	def __int__(self):
		return self.id #id to be shown when called


