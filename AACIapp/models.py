
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
from django import forms


class WorkerRegistrationForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    hospital = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def save(self):
        data = self.cleaned_data
        user = AACIUser.objects.create_user(email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            is_navigator=False,
            is_worker=True,
            password=data['password1'],
            hospital=data['hospital'])
        user.save()

    def clean_password(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            return False
        return password2

class NavigatorRegistrationForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    phone = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def save(self):
        data = self.cleaned_data
        user = AACIUser.objects.create_user(email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            is_navigator=True,
            is_worker=False,
            password=data['password1'])
        user.save()

    def clean_password(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            return False
        return password2

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, is_navigator, is_worker, password=None, hospital=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not phone:
            raise ValueError('Users must have a phone number')
        
        user = self.model(
            email=UserManager.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            hospital=hospital,
            is_navigator=is_navigator,
            is_worker=is_worker
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    # def create_superuser(self, email, twitter_handle, password):
    #     user = self.create_user(email,
    #         password=password,
    #         twitter_handle=twitter_handle,
    #     )
    #     user.is_admin = True
    #     user.save(using=self._db)
    #     return user
     


class AACIUser(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone = models.CharField(max_length=14)
    hospital = models.CharField(max_length=30, null=True)
    is_navigator = models.BooleanField(default=False)
    is_worker = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
 
    def get_full_name(self):
        # For this case we return email. Could also be User.first_name User.last_name if you have these fields
        return self.first_name + " " + self.last_name
 
    def get_short_name(self):
        # For this case we return email. Could also be User.first_name if you have this field
        return self.first_name
 
    def __unicode__(self):
        return self.email
 
    def has_perm(self, perm, obj=None):
        # Handle whether the user has a specific permission?"
        return True
 
    def has_module_perms(self, app_label):
        # Handle whether the user has permissions to view the app `app_label`?"
        return True
 
    @property
    def is_staff(self):
        # Handle whether the user is a member of staff?"
        return self.is_admin



class Appointment(models.Model):
    patient_first_name=models.CharField(max_length=30)
    patient_last_name=models.CharField(max_length=30)
    # date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    patient_phone = models.CharField(max_length=14)
    hospital = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    patient_language = models.CharField(max_length=30)
    special_instructions = models.CharField(max_length=200)
    # appointment_datetime = models.DateTimeField(auto_now=False,auto_now_add=False)
    is_claimed = models.BooleanField()
    is_canceled = models.BooleanField()
    is_new_patient = models.BooleanField()
    worker = models.ForeignKey(AACIUser, related_name='appointment_worker', blank=True, null=True)
    navigator = models.ForeignKey(AACIUser, related_name='appointment_navigator', limit_choices_to={'is_navigator':True}, blank=True, null=True)

class AppointmentForm(ModelForm):
	class Meta:
		model=Appointment
	patient_first_name=forms.CharField(max_length=30)
	patient_last_name=forms.CharField(max_length=30)
	patient_phone = forms.CharField(max_length=14)
	hospital = forms.CharField(max_length=30)
	department = forms.CharField(max_length=30)
	patient_language = forms.CharField(max_length=30)
	special_instructions = forms.CharField(max_length=200)
	#appointment_datetime = forms.DateTimeField(auto_now=False)
