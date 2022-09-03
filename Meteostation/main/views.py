# import dateutil.parser
import json

from django.shortcuts import render
# from django.http import HttpResponse
from .models import Direction
from .models import Data
from django.core.files.storage import FileSystemStorage
from django.db import IntegrityError
from datetime import datetime
# import pytz

from pathlib import Path
import pandas as pd


# Create your views here.


def home(request):
    # objects = Data.objects.all()
    # pass
    # return HttpResponse("<h1>Checking</h1>")
    return render(request, "main/home.html")  # , {'objects': objects})


def data(request):
    params = {}
    if request.method == "POST":
        file = request.FILES.getlist('upload')  # ['upload']
        # print(file)
        # print(file.name)
        # print(file.size)
        fs = FileSystemStorage()

        def create_obj(row, filename):
            date = datetime.strptime(f"{filename}-{row[0]} {row[1]} +0300", '%Y-%m-%d %H:%M:%S %z')
            # print(date)
            # date = datetime.strptime(f"{filename}-{row[0]} {row[1]} +0300", '%Y-%m-%d %H:%M:%S %z')
            # date = datetime.strptime(f"{filename}-{row[0]} {row[1]}", '%Y-%m-%d %H:%M:%S')
            # date = dateutil.parser.parse("{filename}-{row[0]} {row[1]}")

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

            # code = None
            # if f"{row[5]}" == "nan":
            #     code = "CL"
            # else:
            #     code = row[5]
            code = "CL" if f"{row[5]}" == "nan" else row[5]

            # if f"{row[6]}" == "nan":
            #     clouds = 0
            #     clouds = None
            # else:
            #     clouds = int(row[6])
            clouds = None if f"{row[6]}" == "nan" else int(row[6])
            # visibility = None
            # try:
            #     visibility = datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S')
            #     visibility = float(f"{visibility.day}.{visibility.month}")
            # except ValueError:
            #     visibility = float(row[7])
            # if type(row[7]).__name__ == "datetime":
            #     visibility = float(f"{row[7].day}.{row[7].month}")
            # else:
            #     visibility = float(row[7])
            visibility = float(f"{row[7].day}.{row[7].month}" if type(row[7]).__name__ == "datetime" else row[7])

            # if f"{row[8]}" == "nan":
            #     humidity = 0
            # else:
            #     humidity = int(row[8])
            humidity = 0 if f"{row[8]}" == "nan" else int(row[8])
            # humidity = int(row[8])
            pressure = None if f"{row[9]}" == "nan" else int(row[9])

            # if f"{row[10]}" == "nan":
            #     lower_limit = 0
            #     lower_limit = None
            # else:
            #     lower_limit = int(row[10])
            lower_limit = None if f"{row[10]}" == "nan" else int(row[10])
            # lower_limit = int(row[10])
            try:
                Data.objects.create(date=date, temperature=temperature, direction=direction,
                                velocity=velocity, weather_code=code, cloud_amount=clouds,
                                visibility_range=visibility, humidity=humidity, atmo_pressure=pressure,
                                lower_cloud_limit=lower_limit)
            except IntegrityError:
                pass
            # print(date)

        # boolean = False
        for i in file:
            # print(i.name)
            fs.save(i.name, i)
            read_file = pd.read_excel("/main/media/" + i.name)
            # print(type(read_file).__name__)
            # print(read_file)
            filename = Path(i.name).stem
            # try:
            read_file.apply(create_obj, axis=1, args=(filename,))
            # except IntegrityError as e:
            #     boolean = True
        # print(type(read_file.iloc[10]).__name__)
        # print(read_file.iloc[10][1])
        # print(read_file.iloc[0])

        # create_obj(read_file.iloc[1486])
        # create_obj(read_file.iloc[10])

        # try:
        # read_file.apply(create_obj, axis=1)
        # except IntegrityError as e:
        #     print(e.__dict__)
        # Data.objects.all().delete()

        # print(type(read_file.iloc[10, 7]).__name__)
        # print(read_file.iloc[10, 7])
        # result = None
        # try:
        #     result = datetime.strptime(read_file.iloc[10, 7], '%Y-%m-%d %H:%M:%S')
        #     result = float(f"{result.day}.{result.month}")
        # except ValueError as e:
        #     result = float(read_file.iloc[10, 7])
        # print(result, end="; ")
        # print(type(result).__name__)
        # if type(read_file.iloc[10, 7]).__name__ == "datetime":
        # result = float(f"{read_file.iloc[10, 7].day}.{read_file.iloc[10, 7].month}")
        # else:
        # result = float(read_file.iloc[10, 7])
        # print(result)

        # for i in range(11):
        # print(f"{i}. value:{read_file.iloc[0, i]};{type(read_file.iloc[0, i]).__name__}")
        params["message"] = (  # "Duplicate entry denied" if boolean is True else
                             f"File{('s' if len(file) > 1 else '')} successfully uploaded")

    return render(request, "main/data.html", params)
