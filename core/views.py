import json

from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render

from .models import WeatherData
from .tasks import sync_weather as sync_weather_function


def home(request):
    return render(request, 'core/home.html')


def sync_weather(request):
    if request.method == 'POST':
        status = sync_weather_function()
        data = {'status': status}
        data = json.dumps(data)
    else:
        data = 'Error. GET method not allowed'

    return HttpResponse(data, content_type='application/json')


def get_weather(request):
    q = request.GET.get('q')

    if not q:
        data = 'q - required parameter'
        return HttpResponse(data, content_type='application/json')
    q = q.lower()
    try:
        obj = WeatherData.objects.get(q=q)
    except WeatherData.DoesNotExist:
        data = 'q not found'
        return HttpResponse(data, content_type='application/json')

    data = model_to_dict(obj, fields=[field.name for field in obj._meta.fields if field.name not in ['id', 'q']])
    data = json.dumps(data)
    return HttpResponse(data, content_type='application/json')
