# from django.template import Context, loader, RequestContext
# from AACIapp.models import *
# from django.views.decorators.csrf import csrf_protect, csrf_exempt
# from django.shortcuts import render, render_to_response
# from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import Context, loader, Template, RequestContext
from django.template.loader import get_template
from AACIapp.models import *
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

def register_navigator(request, error=None):
    if request.method == 'POST':
        form = NavigatorRegistrationForm(request.POST)
        if form.is_valid():
            if form.clean_password():
                user = form.save()
                return HttpResponseRedirect("/RegistrationComplete")
            else:
                return HttpResponseRedirect("/Register/Password")
    else:
        form = NavigatorRegistrationForm()
    return render_to_response("create_user.html", {
        'form': form, 'error': error, 'worker': False,
    }, context_instance=RequestContext(request))


def register_worker(request, error=None):
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST)
        if form.is_valid():
            if form.clean_password():
                user = form.save()
                return HttpResponseRedirect("/RegistrationComplete")
            else:
                return HttpResponseRedirect("/Register/Password")
    else:
        form = WorkerRegistrationForm()
    return render_to_response("create_user.html", {
        'form': form, 'error': error, 'worker': True,
    }, context_instance=RequestContext(request))

def login_view(request, error=None):
    if request.method=='POST':
        email= request.POST['email']
        password = request.POST['password']
        user=authenticate(email=email,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/Appointments")
            else:
                return HttpResponseRedirect("/Appointments")
        else:
            return render_to_response("login.html", {
            'error': True,
        }, context_instance=RequestContext(request))
    return render_to_response("login.html", {'error':None,},context_instance=RequestContext(request))
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/Login")


def registration_complete(request):
    return render_to_response("registration_complete.html", {},context_instance=RequestContext(request))

def appointment_claimed(request):
    return render_to_response("appointment_claimed.html", {},context_instance=RequestContext(request))

@login_required
def appointments(request):
    if request.method=='POST':
        if 'claimed_appointment' in request.POST:
            appointment_id = request.POST['claimed_appointment']
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.is_claimed = True
            appointment.navigator=request.user
            appointment.save()
            return HttpResponseRedirect("/AppointmentClaimed")
        if 'cancel_appointment' in request.POST:
            appointment_id = request.POST['cancel_appointment']
            appointment = Appointment.objects.get(id=appointment_id)
            appointment.is_canceled = True
            appointment.save()
        if 'edit_appointment' in request.POST:
            return edit_appointment(request)
        if 'save_appointment_edits' in request.POST:
            save_appointment_edits(request.POST)

    query_results = Appointment.objects.all()
    appointments = []
    for appointment in query_results:
        if request.user.is_worker and appointment.worker == request.user:
            appointments.append([appointment,True])
        elif request.user.is_worker:
            appointments.append([appointment,False])
        elif request.user.is_navigator:
            appointments.append([appointment,]) 
    c = Context({'appointments': appointments, 'user':request.user})
    return render_to_response("appointments.html", c, context_instance=RequestContext(request))

@csrf_exempt
def create_appointment(request):
    t = loader.get_template('newappointment.html')
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            appointment = Appointment.objects.latest('id')
            appointment.worker = request.user
            appointment.save()
        else:
            return HttpResponseRedirect('/NotVAlid')
        return HttpResponseRedirect('/ProcessAppointment')
    else:
        form = AppointmentForm()
        return HttpResponse(t.render(Context({'worker':request.user.id})))
        # form = AppointmentForm()
        # t = loader.get_template('newappointment.html')
        # return render_to_response(t, {'form':form}, context_instance=RequestContext(request))
    #return render_to_response(t, {}, context_instance=RequestContext(request))

def edit_appointment(request):
    appointment = Appointment.objects.get(id=request.POST['edit_appointment'])
    return render_to_response("edit_appointment.html", {'appointment':appointment}, context_instance=RequestContext(request))

def save_appointment_edits(appointment_edits):
    appointment = Appointment.objects.get(id=appointment_edits['appointment_id'])
    appointment.patient_first_name = appointment_edits['patient_first_name']
    appointment.patient_last_name = appointment_edits['patient_last_name']
    appointment.patient_phone = appointment_edits['patient_phone']
    appointment.hospital = appointment_edits['hospital']
    appointment.department = appointment_edits['department']
    appointment.patient_language = appointment_edits['patient_language']
    appointment.special_instructions = appointment_edits['special_instructions']
    appointment.save()


@csrf_exempt
def process_appointment(request):
    t = loader.get_template('processForm.html')
    #return render(request, t , {'form': form,})
    return HttpResponse(t.render(Context({})))