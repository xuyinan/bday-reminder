from django.shortcuts import render, render_to_response

import os
from django.http import HttpResponse
from django.template import Template, Context, RequestContext
from django.template.loader import get_template


# Create your views here.
def login(request):
    return render_to_response("registration/login.html", {}, context_instance=RequestContext(request))