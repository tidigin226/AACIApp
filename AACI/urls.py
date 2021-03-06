from django.conf.urls import patterns, include, url
from AACI.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',('^CreateAppointments$', create_appointment),
	('^ProcessAppointment$', process_appointment),
	('^Appointments$', appointments),
	('^RegistrationComplete$', registration_complete),
	('^Register/Worker$', register_worker),
	('^Register/Navigator$', register_navigator),
	('^AppointmentClaimed$', appointment_claimed),
	('^Login$',login_view),
	('^Logout$', logout_view),
    # Examples:
    # url(r'^$', 'AACI.views.home', name='home'),
    # url(r'^AACI/', include('AACI.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
