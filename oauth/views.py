from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, Template, Context



CLIENT_ID = 'DAyqL3V0kx75qqlvXg2xtKkClIFnakst3X3ONl9y'
CLIENT_SECRET = 'JlIH0L5bTDKLSJWaZpyoGSMPu7HLEShGKZQdQX3KWXyYlyTwBvlrRa4V6IwAMO3UNH6KlBrhajeumrtLm6JkZWCsO4X3qChYYLKhfJ8zZNvQkEkF00FEATBCSLnNtEFt'
# CALLBACK_URI = 'http://yinanxu.pythonanywhere.com/bthapi/oauth/drchrono/login/done'
CALLBACK_URI = 'http://yinanxu.pythonanywhere.com/rango'

BASE_URL = 'https://drchrono.com'


# Create your views here.

def _get_referer_url(request):
    referer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/'
    return referer_url


import urllib
import urllib2
import json
import requests

def drchrono_login(request):
    print request

    # get authorization
    auth_url = BASE_URL + '/o/authorize/'
    parameters = urllib.urlencode({
                     'response_type': 'code',
                     'client_id': CLIENT_ID,
                     'redirect_uri': CALLBACK_URI,
                     'state': _get_referer_url(request)
                 })
    drchrono_auth_url = '%s?%s' % (auth_url, parameters)
    # print drchrono_auth_url

    req = requests.get(auth_url, parameters)
    # print req.text
    # resp = urllib2.urlopen(req)
    # print resp.read()

    # data = json.loads(resp.read())
    
    
    response = None
    
    return HttpResponseRedirect(drchrono_auth_url)
    print response
    # get access_token



    # direct to callback uri
    
    return HttpResponse("you are successful")



def get_access_token(code):
    auth_url = BASE_URL + '/o/token/'
    body = urllib.urlencode({
                'code': code, # code
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'redirect_uri': CALLBACK_URI,
                'grant_type': 'authorization_code' # must be this value
                })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    req = urllib2.Request(auth_url, body, headers)
    resp = urllib2.urlopen(req)
     
    data = json.loads(resp.read())
    
    return data['access_token']



def get_user_info(access_token):

    # response = requests.get('https://drchrono.com/api/users/current', headers={
    # 'Authorization': 'Bearer %s' % access_token,
    # })
    # response.raise_for_status()
    # data = response.json()

    # # You can store this in your database along with the tokens
    # username = data['username']

    if access_token:
        response = requests.get('https://drchrono.com/api/users/current', headers={
        'Authorization': 'Bearer %s' % access_token,
        })
        response.raise_for_status()
        data = response.json()

        # You can store this in your database along with the tokens
        username = data['username']
        print username

        # userinfo_url = BASE_URL + '/api/users'
        # query_string = urllib.urlencode({'access_token': access_token})
         
        # resp = urllib2.urlopen("%s?%s" % (userinfo_url, query_string))
        # data = json.loads(resp.read())
         
        return data


def drchrono_auth(request):
    print request.GET
     
    if 'error' in request.GET or 'code' not in request.GET:
        return HttpResponseRedirect('/reminder/')
     
    code = request.GET['code']
     
    access_token = get_access_token(code)
    print access_token
    userinfo = get_user_info(access_token)
    print userinfo
     
    # request.session['blog_user'] = blog_user
     
    next = '/reminder/'
    print next
    # if 'state' in request.GET:
    #     next = request.GET['state']
    #     print next
     
    return HttpResponseRedirect(next)





