from django.shortcuts import render
# from django.http import HttpResponse
from .models import Data


# Create your views here.


def home(request):
    # objects = Data.objects.all()
    # pass
    # return HttpResponse("<h1>Checking</h1>")
    return render(request, "main/home.html")  # , {'objects': objects})


def data(request):
    return render(request, "main/data.html")

