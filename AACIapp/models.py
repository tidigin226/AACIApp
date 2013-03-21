
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

class Appointment(models.Model):
	patient_first_name=models.CharField(max_length=30)
	patient_last_name=models.CharField(max_length=30)
	patient_phone = models.CharField(max_length=14)
	hospital = models.CharField(max_length=30)
	department = models.CharField(max_length=30)
	patient_language = models.CharField(max_length=30)
	special_instructions = models.TextField()
	# appointment_datetime = models.DateTimeField(auto_now=False,auto_now_add=False)
	is_claimed = models.BooleanField()
	#volunteer = models.ForeignKey()

class AppointmentForm(ModelForm):
	class Meta:
		model=Appointment
	# patient_first_name=forms.CharField(max_length=30)
	# patient_last_name=forms.CharField(max_length=30)
	# patient_phone = forms.CharField(max_length=14)
	# hospital = forms.CharField(max_length=30)
	# department = forms.CharField(max_length=30)
	# patient_language = forms.CharField(max_length=30)
	# special_instructions = forms.TextField()
	# appointment_datetime = forms.DateTimeField(auto_now=False,auto_now_add=False)


class Worker(models.Model):
	user = models.OneToOneField(User)
	worker_first_name=models.CharField(max_length=30)
	worker_last_name=models.CharField(max_length=30)
	worker_phone = models.CharField(max_length=14)
	worker_email = models.EmailField(max_length=40)
	hospital = models.CharField(max_length=30)

class WorkerForm(ModelForm):
	class Meta:
		model=Worker

class Volunteer(models.Model):
	user = models.OneToOneField(User)
	volunteer_first_name=models.CharField(max_length=30)
	volunteer_last_name=models.CharField(max_length=30)
	volunteer_phone = models.CharField(max_length=14)
	volunteer_email = models.EmailField(max_length=40)