import requests
from core.models import WeatherData

CITY_LIST = ['London', 'Paris']
APP_ID = '1550e337d66dd8bd59481fd930e661e0'


def gen_link(q):
    version = '2.5'
    url = 'http://api.openweathermap.org/data/{}/weather?q={}&APPID={}'
    return url.format(version, str(q), APP_ID)


def sync_weather():
    status = []
    for q in CITY_LIST:
        try:
            q = q.lower().strip()
            response = requests.get(gen_link(q))
            data = response.json()

            data = {
                'current_temp': data['main'].get('temp', ''),
                'temp_min': data['main'].get('temp_min', ''),
                'temp_max': data['main'].get('temp_max', ''),
                'wind_speed': data.get('wind', {}).get('speed', ''),
                'weather_condition': data.get('weather', [{}])[0].get('description', ''),
            }

            try:
                obj = WeatherData.objects.get(q=q)
                for key, value in data.items():
                    setattr(obj, key, value)
                obj.save()
            except WeatherData.DoesNotExist:
                new_values = {'q': q}
                new_values.update(data)
                obj = WeatherData(**new_values)
                obj.save()

            status.append(True)
        except:
            status.append(False)

    return 'ok' if all(status) else 'error'
