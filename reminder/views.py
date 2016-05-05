from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template, Context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template

import requests, datetime, json

# from reminder.forms import UserForm, UserProfileForm
from oauth.models import OauthUserProfile
from reminder.models import DoctorProfile, PatientProfile, LogHistory
from utils import send_email


TEST_WEBSITE = True

# Create your views here.
def index(request):
    context_dict = {}
    context = RequestContext(request)

    # if TEST_WEBSITE:
    #     request.session['username'] = 'yinanxu'

    if 'username' in request.session:
        context_dict['username'] = request.session['username']
    else:
        return HttpResponseRedirect('/oauth/drchrono/login/')

    return render_to_response('index.html', context_dict, context)


def user_signin(request):
    context_dict = {}
    context = RequestContext(request)
    return HttpResponseRedirect('/oauth/drchrono/login/')


def user_signup(request):
    return HttpResponseRedirect('https://www.drchrono.com/pricing-details/#signup')


def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    # logout(request)
    try:
        OauthUserProfile.objects.get(username=request.session['username']).delete()
        request.session.pop('username')
    except Exception, e:
        None

    # Take the user back to the homepage.
    return HttpResponseRedirect('/reminder/')


def about(request):
    context_dict = {}
    context = RequestContext(request)

    if 'username' in request.session:
        context_dict['username'] = request.session['username']

    return render_to_response('about.html', context_dict, context)


def contact(request):
    context_dict = {}
    context = RequestContext(request)

    if 'username' in request.session:
        context_dict['username'] = request.session['username']

    errors = []
    if request.method == 'POST':
        if not request.POST.get('name', ''):
            errors.append('Enter your name.')
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            send_email(
                name=request.POST['name'], 
                subject=request.POST['subject'],
                message=request.POST['message'],
                resp_addr=request.POST.get('email'), 
                contact=True
            )
            return HttpResponseRedirect('/reminder/contact/thanks/')

    context_dict['errors'] = errors
    return render_to_response('contact.html', context_dict, context)


def contact_thanks(request):
    context_dict = {}
    context = RequestContext(request)

    if 'username' in request.session:
        context_dict['username'] = request.session['username']

    return render_to_response('contact_thanks.html', context_dict, context)


def use_system(request):
    context_dict = {}
    context = RequestContext(request)

    # Insert Patients List to PatientProfile Table which will be used in the following two pages. 
    user = OauthUserProfile.objects.get(username=request.session['username'])

    # query doctor profile 
    doctor = DoctorProfile.objects.get(username=request.session['username'])
    # render the authorization to send emails
    is_doctor = doctor.is_doctor
    context_dict['is_doctor'] = is_doctor
    # This is user is not a doctor
    if not is_doctor:
        return render_to_response('use_system.html', context_dict, context)

    # No user exist in OauthUserProfile, redirect to login page
    if not user:
        return HttpResponseRedirect('/oauth/drchrono/login/')
    
    # request Patients from API
    patients = []
    request_success = False

    access_token = user.access_token
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }

    patients_url = 'https://drchrono.com/api/patients'
    try:
        while patients_url:
            data = requests.get(patients_url, headers=headers).json()
            patients.extend(data['results'])
            patients_url = data['next'] # A JSON null on the last page
        request_success = True
    except Exception, e:
        request_success = False


    if request_success:
        if doctor.num_of_patients == len(patients):
            # no number of patients change, reduce IO of database
            '''But this should be fixed (reduce and increase the same # of patients)'''
            print '-----no number of patients change-----'
            pass
        else:
            for patient in patients:
                name = patient['first_name'] + ' ' + patient['last_name']
                date_of_birth = patient['date_of_birth']
                email = patient['email']
                cell_phone = patient['cell_phone']
                # create or renew patient profile
                PatientProfile.objects.get_or_create(
                    name = name,
                    doctor = doctor,
                    date_of_birth = date_of_birth,
                    email = email, 
                    cell_phone = cell_phone
                )
            doctor.num_of_patients = len(patients)
            doctor.save()

    return render_to_response('use_system.html', context_dict, context)


def birthday_email_send(request):
    # only need to qquery in the database, no need to request from the API again. 
    context_dict = {}
    context = RequestContext(request)
    today = datetime.date.today()
    today = today.strftime("%m-%d")

    if TEST_WEBSITE:
        today = '09-09'

    if 'username' in request.session:
        context_dict['username'] = request.session['username']
        doctor = DoctorProfile.objects.get(username=request.session['username'])
        patients = PatientProfile.objects.filter(doctor=doctor)
        if patients:
            patients_birthday_today = []
            patients_without_birthday = []
            for patient in patients:
                if patient.date_of_birth:
                    birthday = datetime.datetime.strptime(patient.date_of_birth, '%Y-%m-%d')
                    birthday = birthday.strftime("%m-%d")
                    if birthday == today:
                        print birthday
                        patients_birthday_today.append(patient)
                else:
                    patients_without_birthday.append(patient)

            context_dict['doctor'] = doctor
            context_dict['patients_birthday_today'] = patients_birthday_today
            context_dict['patients_without_birthday'] = patients_without_birthday

    return render_to_response('birthday_email.html', context_dict, context)


def birthday_email_done(request):
    context_dict = {}
    context = RequestContext(request)

    if request.method == 'POST':
        patients_list = request.POST.getlist('patients_chosen', [])

        # patients_list = patients_list[1]
        
        patients_with_email = []
        patients_without_email = []
        doctor = DoctorProfile.objects.get(username=request.session['username'])
        for patient_name in patients_list:
            patient = PatientProfile.objects.filter(name=patient_name, doctor=doctor)[0]
            if patient.email:
                email = patient.email
                patients_with_email.append(patient)
                send_email(name=patient_name,
                    doctor_name=doctor.username, 
                    subject='Happy Birthday', 
                    to_addr=email,
                    birthday=True)

            else:
                patients_without_email.append(patient)
        context_dict['patients_with_email'] = patients_with_email
        context_dict['patients_without_email'] = patients_without_email
        context_dict['birthday_flag'] = True

    return render_to_response('use_system_done.html', context_dict, context)


def custom_email(request):
    context_dict = {}
    context = RequestContext(request)

    if 'username' in request.session:
        context_dict['username'] = request.session['username']
        doctor = DoctorProfile.objects.get(username=request.session['username'])
        patients = PatientProfile.objects.filter(doctor=doctor)
        context_dict['doctor'] = doctor
        context_dict['patients'] = patients

    return render_to_response('custom_email.html', context_dict, context)


def custom_email_send(request):
    context_dict = {}
    context = RequestContext(request)

    if request.method == 'POST':
        patients_chosen = request.POST.getlist('patients_chosen')
        request.session["patients_chosen"] = patients_chosen

    return render_to_response('custom_email_send.html', context_dict, context)


def custom_email_done(request):
    context_dict = {}
    context = RequestContext(request)

    if request.method == 'POST':
        patients = request.session["patients_chosen"]
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        patients_with_email = []
        patients_without_email = []
        doctor = DoctorProfile.objects.get(username=request.session['username'])
        for patient_name in patients:
            patient = PatientProfile.objects.filter(name=patient_name, doctor=doctor)[0]
            if patient.email:
                email = patient.email
                patients_with_email.append(patient)
                send_email(subject=subject, message=message, to_addr=email)
            else:
                patients_without_email.append(patient)
        context_dict['patients_with_email'] = patients_with_email
        context_dict['patients_without_email'] = patients_without_email
        context_dict['birthday_flag'] = False

    return render_to_response('use_system_done.html', context_dict, context)


