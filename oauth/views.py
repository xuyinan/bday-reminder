from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template, Context
import urllib, urllib2
import requests
import json
import datetime, pytz

from oauth.models import OauthUserProfile


CALLBACK_URI = 'http://yinanxu.pythonanywhere.com/oauth/drchrono/login/done'

# credential for Drchrono
CLIENT_ID = 'DAyqL3V0kx75qqlvXg2xtKkClIFnakst3X3ONl9y'
CLIENT_SECRET = 'JlIH0L5bTDKLSJWaZpyoGSMPu7HLEShGKZQdQX3KWXyYlyTwBvlrRa4V6IwAMO3UNH6KlBrhajeumrtLm6JkZWCsO4X3qChYYLKhfJ8zZNvQkEkF00FEATBCSLnNtEFt'
BASE_URL = 'https://drchrono.com'
AUTHORIZE_URL = BASE_URL + '/o/authorize'
ACCESS_TOKEN_URL = BASE_URL + '/o/token/'
USER_URL = BASE_URL + '/api/users'


# BASE_URL = 'https://drchrono.com'
http_proxy = 'proxy.server:3128'
proxy = {'http': http_proxy}
HOMEPAGE = '/reminder/'

# Create your views here.

def _get_referer_url(request):
    referer_url = request.META.get('HTTP_REFERER', HOMEPAGE)
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = HOMEPAGE
    return referer_url



def drchrono_login(request):
    auth_url = AUTHORIZE_URL
    parameters = urllib.urlencode({
                     'response_type': 'code',
                     'client_id': CLIENT_ID,
                     'redirect_uri': CALLBACK_URI,
                     'state': _get_referer_url(request)
                 })
    drchrono_auth_url = '%s?%s' % (auth_url, parameters)
    return HttpResponseRedirect(drchrono_auth_url)


def get_access_token(code):


    auth_url = ACCESS_TOKEN_URL
    data = {
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': CALLBACK_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }

    response = requests.post(auth_url, data)
    # {"access_token": "wDECg2oPibe6CgGn57aVcB4z4kZ42R", "token_type": "Bearer", "expires_in": 172800, "refresh_token": "FgYFSureOVA7PKWwy90JRf90SdZBSc", "scope": "user:write messages:read labs:write patients:write billing:write user:read labs:read patients:read calendar:write labs patients:summary:write patients patients:summary:read user clinical:read billing:read messages:write clinical:write calendar patients:summary calendar:read"}
    print response.content
    response.raise_for_status()
    data = response.json()

    # Save these in your database associated with the user
    access_token = data['access_token']
    refresh_token = data['refresh_token']
    expires_timestamp = datetime.datetime.now(pytz.utc) + datetime.timedelta(seconds=data['expires_in'])

    return (access_token, refresh_token, expires_timestamp)


def get_username(access_token):
    username = None
    if access_token:
        response = requests.get('https://drchrono.com/api/users/current', headers={
            'Authorization': 'Bearer %s' % access_token,
        })
        response.raise_for_status()
        data = response.json()

        # You can store this in your database along with the tokens
        username = data['username']

    return username


def drchrono_auth(request):

    # if 'username' in request.session:
    #     return HttpResponseRedirect(HOMEPAGE)

    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseRedirect('/reminder/')

    code = request.GET['code']

    access_token, refresh_token, expires_timestamp = get_access_token(code)
    # print 'access_token', access_token
    username = get_username(access_token)
    print username


    # get USER
    user = OauthUserProfile.objects.get(username=username)
    if not user:
        # create USER
        '''
        OauthUserProfile.objects.create(
            username='yinanxu', 
            access_token='access_token', 
            refresh_token='refresh_token', 
            expires_timestamp=datetime.datetime.now()
        )
        '''
        OauthUserProfile.objects.create(
            username=username, 
            access_token=access_token, 
            refresh_token=refresh_token, 
            expires_timestamp=expires_timestamp
        )
    else:
        # renew USER
        user.access_token = access_token
        user.refresh_token=refresh_token
        user.expires_timestamp=expires_timestamp
        user.save()

    # request.session['username'] = username

    next = HOMEPAGE
    # if 'state' in request.GET:
    #     next = request.GET['state']

    return HttpResponseRedirect(HOMEPAGE)



