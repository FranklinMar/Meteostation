from .models import Direction
from .models import Data
from .models import Region
from .forms import UploadFileForm

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.db import IntegrityError
# from django.views.generic import *
from django.views.decorators.cache import never_cache
# from django.http import HttpResponse

from datetime import datetime

from pathlib import Path
import pandas as pd


# Create your views here.

# class TableView(DetailView):
#     model = Region
#     template_name = 'main/table.html'
#     context_object_name = 'region'
#     slug_field = 'name'
#     slug_url_kwarg = 'name'


def home(request):
    # objects = Data.objects.all()
    # pass
    # return HttpResponse("<h1>Checking</h1>")
    return render(request, "main/home.html")  # , {'objects': objects})


def create_obj(row, filename, region_data):
    date = datetime.strptime(f"{filename}-{row[0]} {row[1]} +0300", '%Y-%m-%d %H:%M:%S %z')
    temperature = 0 if f"{row[2]}" == "nan" else int(row[2])

    directions = Direction.objects.get
    direction = directions(direction="Calm")
    if row[3] == "Переменный":
        direction = directions(direction="Variable")
    elif row[3] == "Северный":
        direction = directions(direction="North")
    elif row[3] == "С-В":
        direction = directions(direction="North-East")
    elif row[3] == "Восточный":
        direction = directions(direction="East")
    elif row[3] == "Ю-В":
        direction = directions(direction="South-East")
    elif row[3] == "Южный":
        direction = directions(direction="South")
    elif row[3] == "Ю-З":
        direction = directions(direction="South-West")
    elif row[3] == "Западный":
        direction = directions(direction="West")
    elif row[3] == "С-З":
        direction = directions(direction="North-West")

    velocity = 0 if f"{row[4]}" == "nan" else int(row[4])
    code = "CL" if f"{row[5]}" == "nan" else row[5]
    clouds = None if f"{row[6]}" == "nan" else int(row[6])
    visibility = float(f"{row[7].day}.{row[7].month}" if type(row[7]).__name__ == "datetime" else row[7])
    humidity = 0 if f"{row[8]}" == "nan" else int(row[8])
    pressure = None if f"{row[9]}" == "nan" else int(row[9])
    lower_limit = None if f"{row[10]}" == "nan" else int(row[10])
    try:
        datas = Data.objects.create(date=date, temperature=temperature, direction=direction,
                            velocity=velocity, weather_code=code, cloud_amount=clouds,
                            visibility_range=visibility, humidity=humidity, atmo_pressure=pressure,
                            lower_cloud_limit=lower_limit)
        region_data.add(datas)
    except IntegrityError:
        pass


@never_cache
# def table(request):
def table(request, name=None):
    params = {}
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.getlist('file')  # ['upload']
            print(file)
            if len(file) == 0:
                file = [request.FILES['file']]
            print(file)
            # print(file.name)
            # print(file.size)
            # region = request.POST.get('region')
            region = Region.objects.get(name__exact=name).datas
            # file = request.FILES.getlist('upload')  # .POST.get('upload')
            # print(type(file).__name__)
            fs = FileSystemStorage()
            # print(len(file))

            for i in file:
                fs.save(i.name, i)
                read_file = pd.read_excel("/main/media/" + i.name)
                filename = Path(i.name).stem
                print(i)
                read_file.apply(create_obj, axis=1, args=(filename, region))
            params["message"] = f"File{('s' if len(file) > 1 else '')} successfully uploaded"
    else:
        form = UploadFileForm()
    params["form"] = form
    params["name"] = name
    params["data"] = Region.objects.get(name__exact=name).datas.all() if name else None  # Data.objects.all()  # [0:70]
    # lviv = Region.objects.get(name="Lviv")
    # lviv.offset_y = -10
    # lviv.save()
    # lviv = Region.objects.get(name="Lviv").datas
    # for datas in params["data"]:
    #     lviv.add(datas)
    params["dictionary"] = {
        0: "Clear",
        1: "Low",
        2: "Low",
        3: "Light",
        4: "Light",
        5: "Variable",
        6: "Variable",
        7: "Variable",
        8: "Clearing",
        9: "Clearing",
        10: "Full/Solid"
    }
    params["codes"] = {
        "CL": "Clear",
        "BL": "Haze",
        "BR": "Haze",
        "FG": "Fog",
        "SNRA": "Snow with rain",
        "SH": "Heavy ",
        "RA": "Rain",
        "SN": "Snow",
        "TS": "Thunderstorm",
        "DZ": "Drizzle",
        "FZ": "Ice",
        "HL": "Hail",
        "+": " and "
    }
    return render(request, "main/table.html", params)


# def regions(request):
#     return render(request, "main/data.html", {regions: Region.objects.all()})


@never_cache
def data(request):
    return render(request, "main/data.html", {"regions": Region.objects.all()})
    # params = {}
    # if request.method == "POST":
    #     file = request.FILES.getlist('upload')
    #     fs = FileSystemStorage()
    #
    #     for i in file:
    #         fs.save(i.name, i)
    #         read_file = pd.read_excel("/main/media/" + i.name)
    #         filename = Path(i.name).stem
    #         read_file.apply(create_obj, axis=1, args=(filename,))
    #     params["message"] = f"File{('s' if len(file) > 1 else '')} successfully uploaded"
    # return render(request, "main/data.html", params)
