from django.shortcuts import render

# Create your views here.


def landingPage_view(request):
    return render(request, "home.html")