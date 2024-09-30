from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home_view(*args, **kwargs):
    return "<h1> Home Page </h1>"

def about_view(*args, **kwargs):
    return HttpResponse("<h1> About </h1>")