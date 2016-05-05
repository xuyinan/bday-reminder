from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template, Context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template


import requests, datetime, json

from bthapi import settings
from oauth.models import OauthUserProfile
from reminder.models import DoctorProfile, PatientProfile, LogHistory
from reminder.utils import send_email


TEST_WEBSITE = settings.DEBUG

# Create your views here.
def index(request):
    context_dict = {}
    context = RequestContext(request)

    # If username in request.session, you are logged in. DISPLAY 'logout' menu.
    # Otherwise, DISPLAY 'login' menu. 
    if 'username' in request.session:
        context_dict['username'] = request.session['username']

    return render_to_response('index.html', context_dict, context)


def user_signin(request):
    context_dict = {}
    context = RequestContext(request)

    if TEST_WEBSITE:
        # DEBUG module on 'http://127.0.0.1:8000', save 'yinanxu' in request.session
        request.session['username']='yinanxu'
        # Redirect to Homepage
        return HttpResponseRedirect('/reminder/')
    else:
        # Real situation, redirect to 'login' page
        return HttpResponseRedirect('/oauth/drchrono/login/')


def user_signup(request):
    # Redirect to 'signup' page of Drchrono
    return HttpResponseRedirect('https://www.drchrono.com/pricing-details/#signup')


def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    # logout(request)
    try:

        if not TEST_WEBSITE:
            # Delete user profile in OauthUserProfile table
            OauthUserProfile.objects.filter(username=request.session['username']).delete()
        # Delete value of 'username' in request.session
        request.session.pop('username')
    except Exception, e:
        print "logout error-------------------"
        None

    # Take the user back to the homepage.
    return HttpResponseRedirect('/reminder/')


def about(request):
    context_dict = {}
    context = RequestContext(request)

    # If username in request.session, you are logged in. DISPLAY 'logout' menu.
    # Otherwise, DISPLAY 'login' menu. 
    if 'username' in request.session:
        context_dict['username'] = request.session['username']

    return render_to_response('about.html', context_dict, context)


def contact(request):
    context_dict = {}
    context = RequestContext(request)

    # If username in request.session, you are logged in. DISPLAY 'logout' menu.
    # Otherwise, DISPLAY 'login' menu. 
    if 'username' in request.session:
        context_dict['username'] = request.session['username']

    errors = []
    if request.method == 'POST':
        # Check 'subject' field (required)        
        if not request.POST.get('subject', ''):
            errors.append('Enter a subject.')
        # Check 'message' field (required) 
        if not request.POST.get('message', ''):
            errors.append('Enter a message.')
        # Check whether input 'email' valid
        if request.POST.get('email') and '@' not in request.POST['email']:
            errors.append('Enter a valid e-mail address.')
        if not errors:
            # No errors, send contact email
            send_email(
                name=request.POSTget('name'), 
                subject=request.POST['subject'],
                message=request.POST['message'],
                resp_addr=request.POST.get('email'), 
                contact=True
            )
            # Redicrect to 'thanks' page. 
            return HttpResponseRedirect('/reminder/contact/thanks/')

    # if errors, redirect to 'contact' page to re-input information
    context_dict['errors'] = errors
    return render_to_response('contact.html', context_dict, context)


def contact_thanks(request):
    context_dict = {}
    context = RequestContext(request)

    # If username in request.session, you are logged in.
    if 'username' in request.session:
        context_dict['username'] = request.session['username']

    return render_to_response('contact_thanks.html', context_dict, context)


def use_system(request):
    context_dict = {}
    context = RequestContext(request)

    # If username not in request.session, Redirect to 'login' page. Because only 
    # valid user can use this system. 
    if 'username' not in request.session:
        return HttpResponseRedirect('/reminder/signin/')

    context_dict['username'] = request.session['username']

    # query user profile from OauthUserProfile table to get ACCESS_TOKEN
    user = OauthUserProfile.objects.filter(username=request.session['username'])
    # No user exist in OauthUserProfile, redirect to login page
    if not user:
        return HttpResponseRedirect('/oauth/drchrono/login/')

    # query doctor profile 
    doctor = DoctorProfile.objects.get(username=request.session['username'])
    # render the authorization to send emails
    context_dict['is_doctor'] = doctor.is_doctor
    # This is user is not a doctor (no authorization for this system). Return the same
    # page to tell user. 
    if not doctor.is_doctor:
        return render_to_response('use_system.html', context_dict, context)
    
    
    patients = []
    # flag of request success
    request_success = False

    access_token = user[0].access_token
    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }

    # request Patients from API
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
            # Insert Patients List to PatientProfile Table which will be used in 'Birthday' 
            # and 'Custom' email page. 
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
    # only need to query in the database, no need to request from the API again. 
    context_dict = {}
    context = RequestContext(request)
    today = datetime.date.today()
    today = today.strftime("%m-%d")

    if TEST_WEBSITE:
        today = '09-09'

    if 'username' in request.session:
        context_dict['username'] = request.session['username']
        # query doctor profile whose username is in request.session
        doctor = DoctorProfile.objects.get(username=request.session['username'])
        # query all patients whose doctors are the same as lase query
        patients = PatientProfile.objects.filter(doctor=doctor)
        if patients:
            # if exits patients, do something
            patients_birthday_today = []
            patients_without_birthday = []
            for patient in patients:
                if patient.date_of_birth:
                    # patients have 'date_of_birth' in their profile
                    birthday = datetime.datetime.strptime(patient.date_of_birth, '%Y-%m-%d')
                    birthday = birthday.strftime("%m-%d")
                    if birthday == today:
                        # check patient's birthday is today?
                        print birthday
                        patients_birthday_today.append(patient)
                else:
                    # patients have 'date_of_birth' in their profile
                    patients_without_birthday.append(patient)

            context_dict['doctor'] = doctor
            context_dict['patients_birthday_today'] = patients_birthday_today
            context_dict['patients_without_birthday'] = patients_without_birthday
            
    return render_to_response('birthday_email.html', context_dict, context)


def birthday_email_done(request):
    context_dict = {}
    context = RequestContext(request)

    if request.method == 'POST':
        # patients chosen from 'birthday_email' page, only contain patient name
        patients_list = request.POST.getlist('patients_chosen', [])
        
        patients_with_email = []
        patients_without_email = []

        # query doctor profile
        doctor = DoctorProfile.objects.get(username=request.session['username'])
        for patient_name in patients_list:
            # query patient profile in chosen 'patients_list' 
            patient = PatientProfile.objects.filter(name=patient_name, doctor=doctor)[0]
            if patient.email:
                # patient has email in their profile
                email = patient.email
                patients_with_email.append(patient)
                send_email(name=patient_name,
                    doctor_name=doctor.username, 
                    subject='Happy Birthday', 
                    to_addr=email,
                    birthday=True)

            else:
                # patient does not set email in their profile
                patients_without_email.append(patient)

        # Add this message to message history
        patients_name = [patient.name for patient in patients_with_email]
        LogHistory.objects.create(time=datetime.datetime.now(), 
            doctor=doctor, 
            patients=', '.join(patients_name), 
            birthday_message=True, 
            subject=None, 
            message_path=None
        )

        context_dict['patients_with_email'] = patients_with_email
        context_dict['patients_without_email'] = patients_without_email
        context_dict['birthday_flag'] = True
        context_dict['username'] = request.session['username']

    return render_to_response('use_system_done.html', context_dict, context)


def custom_email(request):
    context_dict = {}
    context = RequestContext(request)

    if 'username' in request.session:
        context_dict['username'] = request.session['username']
        # query doctor profile
        doctor = DoctorProfile.objects.get(username=request.session['username'])
        # query all patients profile whose doctor is in last step
        patients = PatientProfile.objects.filter(doctor=doctor)
        context_dict['doctor'] = doctor
        context_dict['patients'] = patients

    return render_to_response('custom_email.html', context_dict, context)


def custom_email_send(request):
    context_dict = {}
    context = RequestContext(request)

    if request.method == 'POST':
        # patients that have been chosen to send custom email
        patients_chosen = request.POST.getlist('patients_chosen')
        # save these patients in request.session to use in the next page
        request.session["patients_chosen"] = patients_chosen
        context_dict['username'] = request.session['username']

    return render_to_response('custom_email_send.html', context_dict, context)


def custom_email_done(request):
    context_dict = {}
    context = RequestContext(request)

    if request.method == 'POST':
        # patients that have been chosen to send custom email
        patients = request.session["patients_chosen"]
        # subject of email
        subject = request.POST.get('subject')
        # message of email
        message = request.POST.get('message')
        patients_with_email = []
        patients_without_email = []
        # query the doctor profile
        doctor = DoctorProfile.objects.get(username=request.session['username'])
        for patient_name in patients:
            # query patient profile that have been chosen 
            patient = PatientProfile.objects.filter(name=patient_name, doctor=doctor)[0]
            if patient.email:
                # patient has email in their profile
                email = patient.email
                patients_with_email.append(patient)
                send_email(subject=subject, message=message, to_addr=email)
            else:
                # patient does not set email in their profile
                patients_without_email.append(patient)

        # Add this message to message history
        patients_name = [patient.name for patient in patients_with_email]
        LogHistory.objects.create(time=datetime.datetime.now(), 
            doctor=doctor, 
            patients=', '.join(patients_name), 
            birthday_message=False, 
            subject=subject, 
            message_path=None
        )

        context_dict['patients_with_email'] = patients_with_email
        context_dict['patients_without_email'] = patients_without_email
        context_dict['birthday_flag'] = False
        context_dict['username'] = request.session['username']

    return render_to_response('use_system_done.html', context_dict, context)


def message_history(request):
    context_dict = {}
    context = RequestContext(request)

    message_histories = []

    if 'username' in request.session:
        context_dict['username'] = request.session['username']
        # query doctor profile
        doctor = DoctorProfile.objects.get(username=request.session['username'])
        # query the message histories of specified doctor
        message_histories = LogHistory.objects.filter(doctor=doctor)

    context_dict['message_histories'] = message_histories

    return render_to_response('message_history.html', context_dict, context)

