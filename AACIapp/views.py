from django.template import Context, loader
from forms.py import AppointmentForm, WorkerForm
from polls.models import Poll
from django.shortcuts import render
from django.http import HttpResponse

def appointments(request):
	query_results = Appointment.objects.all()
    t = loader.get_template('appointments.html')
    c = Context({
        'query_results': query_results,
    })
    return HttpResponse(t.render(c))

def makeappointments(request):
	t = loader.get_template('newappointments.html')
	if request.method == 'POST': # If the form has been submitted...
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = AppointmentForm() # An unbound form

    return render(request, t , {
        'form': form,})


def makeworker(request):
	query_results = Appointment.objects.all()
	t = loader.get_template('appointments.html')
	c = Context({
	    'query_results': query_results,
	})
	return HttpResponse(t.render(c))