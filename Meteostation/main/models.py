import dateutil
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import QuerySet
import scipy.interpolate as interpolations
import pandas as pd
from django_pandas.io import read_frame

# Create your models here.

class Direction(models.Model):
    direction = models.CharField('Напрям вітру', max_length=10, unique=True)

    def __str__(self):
        return self.direction


# class WeatherCode(models.Model):
#     code = models.CharField('Код погоди', max_length=4)
#
#     def __str__(self):
#         return self.code


class Data(models.Model):
    date = models.DateTimeField('Дата і Час спостереження', unique=True)
    temperature = models.IntegerField('Температура повітря °C')
    # direction = models.CharField('Напрям вітру', max_length=3)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    velocity = models.IntegerField('Середня швидкість вітру', validators=[MinValueValidator(0)])
    weather_code = models.CharField('Код погоди', max_length=20, default="CL")
    # weather_code = models.ForeignKey(WeatherCode, on_delete=models.CASCADE)
    cloud_amount = models.IntegerField('Кількість хмар', null=True, validators=[
        MaxValueValidator(10),
        MinValueValidator(0)
    ])
    visibility_range = models.FloatField('Дальність видимості', validators=[MinValueValidator(0)])
    humidity = models.IntegerField('Відносна вологість повітря', validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    atmo_pressure = models.IntegerField('Атмосферний тиск', validators=[MinValueValidator(0)])
    lower_cloud_limit = models.IntegerField('Нижня межа хмарності', null=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        # verbose_name = 'Data'
        verbose_name_plural = 'Data'


class Region(models.Model):
    name = models.CharField('Область', max_length=20, unique=True, null=True)
    coords = models.TextField('Координати мапи', max_length=4000, null=False, default='')
    datas = models.ManyToManyField(Data, blank=True)
    offset_x = models.FloatField('Відступ X', default=0, null=False)
    offset_y = models.FloatField('Відступ Y', default=0, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Interpolations:

    def __init__(self, data_set):
        self.data_set(data_set)

    # def data_set(self):
    #     return self.__data_set

    def data_set(self, data_set):
        # if not data_set:
        #     raise TypeError("Null is not acceptable for this class")
        if not isinstance(data_set, QuerySet):
            raise TypeError("Model Query Sets")
        self.__data_set = pd.DataFrame.from_records(data_set.values()).iloc[:, 1:]
        self.__dates = self.__data_set[self.__data_set.columns[0]].apply(lambda date: date.value)
        # print(type(dates.iloc[0]).__name__)
        self.__rest_of_table = self.__data_set.loc[:,
                        ~self.__data_set.columns.isin(['date', 'humidity', 'weather_code', 'lower_cloud_limit'])]
        # print(self.__data_set)
        # print(dates)
        # print(rest_of_table)
        # self.__Lagrange = {}
        # self.__Linear = {}
        # self.__Spline = {}
        # print()
        # columns = list(rest_of_table.columns)
        # for column in columns:
        #     print(rest_of_table[column])
        #     self.__Lagrange[column] = interpolations.lagrange(dates, rest_of_table[column])
        #     self.__Linear[column] = interpolations.interp1d(dates, rest_of_table[column], kind='linear')
        #     self.__Spline[column] = interpolations.make_interp_spline(dates, rest_of_table[column])
         # = interpolations.lagrange(list(dates), rest_of_table)
        # self.__Linear = interpolations.interp1d(dates, rest_of_table, kind='linear')

    @classmethod
    def interpolations(cls):
        # print(self.__dict__)
        methods = [name for name, value in vars(cls).items() if isinstance(value, property)]
        # methods = [attribute for attribute in self.__dict__
        #       if not attribute.__contains__('__')
        #       and not callable(getattr(self, attribute))]
        return methods

    @property
    def lagrange(self):
        lagrange = {}
        columns = list(self.__rest_of_table.columns)
        for column in columns:
            lagrange[column] = interpolations.lagrange(self.__dates, self.__rest_of_table[column])
        # return self.__Lagrange(x)
        return lagrange

    @property
    def linear(self):
        linear = {}
        columns = list(self.__rest_of_table.columns)
        for column in columns:
            linear[column] = interpolations.interp1d(self.__dates, self.__rest_of_table[column], kind='linear')
        # return self.__Lagrange(x)
        return linear
        # return self.__Linear(x)

    @property
    def spline(self):
        spline = {}
        columns = list(self.__rest_of_table.columns)
        for column in columns:
            spline[column] = interpolations.make_interp_spline(self.__dates, self.__rest_of_table[column])
        # return self.__Lagrange(x)
        return spline
        # return self.__Spline(x)
