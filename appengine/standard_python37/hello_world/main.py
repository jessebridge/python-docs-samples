# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask
import requests
from firebase import firebase
from datetime import datetime


def get_temperature(json_data):
    temp_in_celcius = json_data['main']['temp']
    return temp_in_celcius


def get_clouds_location(json_data):
    cloud_location = json_data['clouds']['all']
    return cloud_location


def get_humidity(json_data):
    humidity = json_data['main']['humidity']
    return humidity


def get_max_temp(json_data):
    max_temp = json_data['main']['temp_max']
    return max_temp


def get_min_temp(json_data):
    min_temp = json_data['main']['temp_min']
    return min_temp


def get_pressure(json_data):
    pressure = json_data['main']['pressure']
    return pressure


def get_wind_speed(json_data):
    wind_speed = json_data['wind']['speed']
    return wind_speed


def get_timestamp(json_data):
    timestamp = json_data['dt']
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def get_wind_degree(json_data):
    wind_degree = json_data['wind']['deg']
    return wind_degree


def get_weather_type(json_data):
    print(json_data)
    weather_type = json_data['weather'][0]['main']
    return weather_type

def post_to_db(db_location, db_input, item_name, fb):
    print(db_location, db_input)
    fb.put(db_location, item_name, db_input)




# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    city_list = ["Brisbane", "Sydney", "Melbourne", "Adelaide", "Perth", "Canberra"]

    fb = firebase.FirebaseApplication("https://weatherwatchers-9d36d.firebaseio.com/", None)
    for city in city_list:
        units_format = "&units=metric"
        api_address = 'https://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=a10fd8a212e47edf8d946f26fb4cdef8&q='
        final_url = api_address + units_format
        json_data = requests.get(final_url).json()

        # Gather data for each attribute
        clouds = get_clouds_location(json_data)
        humidity = get_humidity(json_data)
        max_temp = get_max_temp(json_data)
        min_temp = get_min_temp(json_data)
        pressure = get_pressure(json_data)
        weather_type = get_weather_type(json_data)
        timestamp = get_timestamp(json_data)
        wind_deg = get_wind_degree(json_data)
        wind_speed = get_wind_speed(json_data)
        temperature = get_temperature(json_data)

        # Location of db structures
        DBLocation = 'https://weatherwatchers-9d36d.firebaseio.com/WeatherStation/' + city + '/CurrentWeatherData'

        # Post to db
        post_to_db(DBLocation, clouds, "Clouds", fb)
        post_to_db(DBLocation, pressure, "Pressure", fb)
        post_to_db(DBLocation, temperature, "CurrentTemperature", fb)
        post_to_db(DBLocation, humidity, "Humidity", fb)
        post_to_db(DBLocation, max_temp, "MaxTemp", fb)
        post_to_db(DBLocation, min_temp, "MinTemp", fb)
        post_to_db(DBLocation, pressure, "Pressure", fb)
        post_to_db(DBLocation, weather_type, "Rain3h", fb)
        post_to_db(DBLocation, timestamp, "TimeStamp", fb)
        post_to_db(DBLocation, wind_deg, "WindDeg", fb)
        post_to_db(DBLocation, wind_speed, "WindSpeed", fb)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
