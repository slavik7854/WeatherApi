from django.db import models


class WeatherData(models.Model):
    q = models.CharField(max_length=30, unique=True)
    current_temp = models.FloatField()
    temp_min = models.FloatField()
    temp_max = models.FloatField()
    wind_speed = models.FloatField()
    weather_condition = models.CharField(max_length=100)

    def __str__(self):
        return self.q
