from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from my_user_profile_app.models import Worker
from my_user_profile_app.models import Volunteer


class WorkerInLine(admin.StackedInline):
	model=Worker
	verbose_name_plural='worker'

class VolunteerInLine(admin.StackedInline):
	model=Volunteer
	verbose_name_plural='volunteer'
class UserAdmin(UserAdmin)
	inlines = (WorkerInLine,VolunteerInLine)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)