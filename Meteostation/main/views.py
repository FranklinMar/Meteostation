from django.shortcuts import render
# from django.http import HttpResponse

# Create your views here.


def home(request):
    # pass
    # return HttpResponse("<h1>Checking</h1>")
    return render(request, "main/home.html")
