from django.shortcuts import render
# from django.http import HttpResponse
from .models import Data
from django.core.files.storage import FileSystemStorage
# from Meteostation.Meteostation.settings import MEDIA_ROOT
import pandas as pd
import os


# Create your views here.


def home(request):
    # objects = Data.objects.all()
    # pass
    # return HttpResponse("<h1>Checking</h1>")
    return render(request, "main/home.html")  # , {'objects': objects})


def data(request):
    if request.method == "POST":
        file = request.FILES['upload']
        print(file.name)
        # print(file.size)
        fs = FileSystemStorage()
        fs.save(file.name, file)
        # read_file = pd.read_excel(os.path.join(MEDIA_ROOT), file.name)
        # print(type(read_file).__name__)
        # print(read_file)

    return render(request, "main/data.html")

