import requests
from aux_data import geo_token, weather_token
import pyowm
from datetime import datetime

degree_sign = u'\N{DEGREE SIGN}'


class CLocationInfo:
    def __init__(self, auto_init=True):
        if auto_init:
            data = self.get_location_info()
            self.country = data["country_name"]
            self.city = data["city"]
            self.zip = data["zip"]
            self.country_code = data["country_code"]
        else:
            self.country = 'Россия'
            self.city = 'Москва'

    @staticmethod
    def get_location_info(ip_req=None):
        return requests.get(
            'http://api.ipstack.com/check', params={
                'access_key': geo_token,
                'format': 1,
            }).json()


class CWeatherInfo:
    directions = ["Северный ветер",
                  "Северный, северо-восточный ветер",
                  "Северо-восточный ветер",
                  "Восточный, северо-восточный ветер",
                  "Восточный ветер",
                  "Восточный, юго-восточный ветер",
                  "Юго-восточный ветер",
                  "Южный ветер",
                  "Южный, юго-западный ветер",
                  "Юго-западный ветер",
                  "Западный, юго-западный ветер",
                  "Западный ветер",
                  "Западный, северо-западный ветер",
                  "Северо-западный ветер",
                  "Северный, северо-западный ветер",
                  "Северный ветер"
                  ]

    def __init__(self):
        self.OWM_TOKEN = weather_token
        self.owm = pyowm.OWM(self.OWM_TOKEN, language='RU')

    def get_detailed_report(self, weather):
        temperature = weather.get_temperature('celsius').get('temp')
        wind_speed = weather.get_wind()['speed']
        if 'deg' in weather.get_wind():  # для некоторых городов скорость ветра не указана
            wind_direction = self.directions[int(weather.get_wind()['deg'] / 22.5) - 1]
        else:
            wind_direction = None

        weather.get_detailed_status().capitalize()
        return [temperature, wind_direction, wind_speed, weather.get_detailed_status().capitalize()]

    def get_tomorrow(self, city):
        '''
        nextday = forecast.get_weather_at(next_day)
        decoded_tomorrow = json.loads(nextday.to_JSON())
        detailed_status_tomorrow = decoded_tomorrow['detailed_status']

        strMsg = 'tomorrows weather for ' + city_name + ': ' + detailed_status_tomorrow.title() + 'temperatures range from ' + str(
            nextday.get_temperature('celsius')['temp_min']) + 'degrees Celsius to ' + str(
            nextday.get_temperature('celsius')['temp_max']) + 'degrees Celsius. Cloud cover will be ' + str(
            decoded_tomorrow['clouds']) + 'percent'
        '''

    def get_weather_list(self, city):
        try:
            obs_point = self.owm.three_hours_forecast(city)
            forecast = obs_point.get_forecast()
            weather_list = forecast.get_weathers()
        except Exception:
            return None
        else:
            return weather_list

    def get_weather(self, city, date_r=None):
        if date_r:
            try:
                print('Start Weather forecasting !')
                obs_point = self.owm.three_hours_forecast('Moscow, RU')
                weather = obs_point.get_weather_at(date_r)
            except Exception as er:
                print('Exception fault!!!', er)
                return None
            else:
                return weather
        try:
            obs_point = self.owm.weather_at_place(city)
            weather = obs_point.get_weather()
        except Exception:
            return None
        else:
            return weather


LOCATION = CLocationInfo(True)
