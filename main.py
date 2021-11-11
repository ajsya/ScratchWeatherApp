#rewritten for scratch2py

import requests
from scratch2py import Scratch2Py
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.environ['API_KEY']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']

s2py = Scratch2Py(username, password)
project = s2py.scratchConnect('597674126')

def getWeather(city):
    api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&units=imperial&appid="+API_KEY
    r = requests.get(api)
    if r.status_code == 200:
        data = r.json()

        # at a quick glance
        location = data['name']
        condition = data['weather'][0]['main']
        description = data['weather'][0]['description']

        # right now
        temperature = data['main']['temp'] #temperature in fahrenheit
        feels_like_temperature = data['main']['feels_like']

        #today
        max_temperature = data['main']['temp_max']
        min_temperature = data['main']['temp_min']
        humidity = data['main']['humidity'] # should be a percent
        cloud_coverage = data['clouds']['all'] # should be a percent

        return location, condition, description, temperature, feels_like_temperature, max_temperature, min_temperature, humidity, cloud_coverage
    elif r.status_code == 404:
        print("Requested location not found!")

        return "Location Not Found"

variables = ['location', 'condition', 'description', 'temp', 'feels like temp', 'max temp', 'min temp', 'humidity', 'cloud coverage']
while True:
    request = project.readCloudVar('request')
    #print(request)
    if request != '1':
        if request == '2':
            print('No new requests.')
        else:    
            print("New request intetified.")
            decoded_request = s2py.decode(request)
            #print(decoded_request)
            #location, condition, description, temperature, feels_like_temperature, max_temperature, min_temperature, humidity, cloud_coverage = getWeather(decoded_request)
            weather = getWeather(decoded_request)
            if weather == "Location Not Found":
                project.setCloudVar('request', '2')
                print("Response submited: Location not Found; Code 2")
            else:
                #print(weather)
                y = 0
                for x in range(0, 9):
                    #print(weather[y])
                    try:
                        project.setCloudVar(variables[y], s2py.encode(weather[y]))
                    except TypeError:
                        project.setCloudVar(variables[y], s2py.encode(str(round(weather[y]))))
                    y += 1
                project.setCloudVar('request', '1')
                print("Response Submited: Date sent; Code 1")

    else:
        print('No new requests.')
    time.sleep(30) 
