from django import forms

class WorkerForm(forms.Form):


class AppointmentForm(forms.Form):
	patient_first_name=forms.CharField(max_length=30)
	patient_last_name=forms.CharField(max_length=30)
	patient_phone = forms.CharField(max_length=14)
	hospital = forms.CharField(max_length=30)
	department = forms.CharField(max_length=30)
	patient_language = forms.CharField(max_length=30)
	special_instructions = forms.TextField()
	appointment_datetime = forms.DateTimeField(auto_now=False,auto_now_add=False)
