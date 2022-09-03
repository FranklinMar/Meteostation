from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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
