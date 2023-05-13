from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import UploadFileForm

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.db import IntegrityError
# from django.views.generic import *
from django.views.decorators.cache import never_cache
# from django.http import HttpResponse

from django.core.paginator import Paginator, PageNotAnInteger
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


@never_cache
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
    clouds = 0 if f"{row[6]}" == "nan" else int(row[6])
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
    # for i in Data.objects.all():
    #     i.cloud_amount = 0 if not i.cloud_amount else i.cloud_amount
    #     i.save()
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
    page_number = request.GET.get("page", 1)
    order = request.GET.get("order", "").replace("desc", "-").replace("asc", "")
    sort = order + request.GET.get("sort", "date")
    limit = request.GET.get("limit", 10)
    # limit = limit if isinstance(page_number, int) and isinstance(limit, int) else None

    try:
        region_data = Region.objects.get(name__exact=name).datas.order_by(sort).all()
        # region_data = Region.objects.get(name__exact=name).datas.all()
    except ObjectDoesNotExist:
        region_data = None

    try:
        # print(type(Region.objects.get(name__exact=name).datas.all()).__name__)
        paginator = Paginator(region_data, per_page=limit)
        # print(paginator.get_page(page_number))
        params["page_obj"] = paginator.get_page(page_number)  # Data.objects.all()  # [0:70]
        params["page_range"] = list(str(i) for i in paginator.get_elided_page_range(page_number, on_each_side=2))
        # print(params["page_range"])
        params["page_number"] = str(params["page_obj"].number)
        # print(list(paginator.get_elided_page_range(page_number, on_each_side=2)))
    except (TypeError, ValueError, PageNotAnInteger):
        params["page_obj"] = None
    # print(type(params["page_obj"].object_list).__name__)
    # params["data"] = paginator.get_page(page_number).object_list
    # print(type(paginator.get_page(page_number).object_list).__name__)
    # print(params["data"])
    # print(params["data"][0].__dict__)
    # print(params["page_obj"].__dict__)
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
    # print(Interpolations.interpolations())
    # print(Interpolations(region_data).lagrange(region_data[0].date))
    return render(request, "main/table.html", params)


# def regions(request):
#     return render(request, "main/data.html", {regions: Region.objects.all()})

@never_cache
def interpolations(request, name=None):
    params = {"name": name}
    try:
        region_data = Region.objects.get(name__exact=name).datas.first()
        # region_data = Region.objects.get(name__exact=name).datas.all()
    except ObjectDoesNotExist:
        region_data = None
    functions = Interpolations(region_data)

    params["interpolations"] = [method.capitalize() for method in functions.interpolations]
    return render(request, "main/interpolations.html", params)

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
