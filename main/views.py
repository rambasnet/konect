from django.shortcuts import render, render_to_response, RequestContext, HttpResponseRedirect
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")

