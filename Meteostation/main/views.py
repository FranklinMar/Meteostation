from .models import Direction
from .models import Data
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.db import IntegrityError
# from django.http import HttpResponse

from datetime import datetime

from pathlib import Path
import pandas as pd


# Create your views here.


def home(request):
    # objects = Data.objects.all()
    # pass
    # return HttpResponse("<h1>Checking</h1>")
    return render(request, "main/home.html")  # , {'objects': objects})


def create_obj(row, filename):
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
        Data.objects.create(date=date, temperature=temperature, direction=direction,
                            velocity=velocity, weather_code=code, cloud_amount=clouds,
                            visibility_range=visibility, humidity=humidity, atmo_pressure=pressure,
                            lower_cloud_limit=lower_limit)
    except IntegrityError:
        pass


def table(request):
    params = {}
    if request.method == "POST":
        file = request.FILES.getlist('upload')
        fs = FileSystemStorage()

        for i in file:
            fs.save(i.name, i)
            read_file = pd.read_excel("/main/media/" + i.name)
            filename = Path(i.name).stem
            read_file.apply(create_obj, axis=1, args=(filename,))
        params["message"] = f"File{('s' if len(file) > 1 else '')} successfully uploaded"
    params["data"] = Data.objects.all()  # [0:70]
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


def data(request):
    params = {}
    if request.method == "POST":
        file = request.FILES.getlist('upload')
        fs = FileSystemStorage()

        for i in file:
            fs.save(i.name, i)
            read_file = pd.read_excel("/main/media/" + i.name)
            filename = Path(i.name).stem
            read_file.apply(create_obj, axis=1, args=(filename,))
        params["message"] = f"File{('s' if len(file) > 1 else '')} successfully uploaded"
    return render(request, "main/data.html", params)
