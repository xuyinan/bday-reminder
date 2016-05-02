from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template, Context
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.template.loader import get_template

import requests

# from reminder.forms import UserForm, UserProfileForm
from oauth.models import OauthUserProfile



TEST_WEBSITE = True


# Create your views here.
def index(request):
    context_dict = {}
    context = RequestContext(request)

    if TEST_WEBSITE:
        context_dict['username'] = 'yinanxu'

    if 'username' in request.session:
        context_dict['username'] = request.session['username']
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

    if TEST_WEBSITE:
        context_dict['username'] = 'yinanxu'

    if 'username' in request.session:
        context_dict['username'] = request.session['username']

    return render_to_response('about.html', context_dict, context)

def contact(request):
    context_dict = {}
    context = RequestContext(request)

    if TEST_WEBSITE:
        context_dict['username'] = 'yinanxu'

    if 'username' in request.session:
        context_dict['username'] = request.session['username']

    return render_to_response('contact.html', context_dict, context)


def use_system(request):
    context_dict = {}
    context = RequestContext(request)

    if TEST_WEBSITE:
        context_dict['username'] = 'yinanxu'

    if 'username' in request.session:
        context_dict['username'] = request.session['username']


    headers = {
        'Authorization': 'Bearer %s' % access_token,
    }

    patients = []
    patients_url = 'https://drchrono.com/api/patients'
    while patients_url:
        data = requests.get(patients_url, headers=headers).json()
        patients.extend(data['results'])
        patients_url = data['next'] # A JSON null on the last page

    context_dict['patients'] = patients


    return render_to_response('index.html', context_dict, context)

    # need to add more code below







