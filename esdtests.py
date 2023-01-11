# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 23:43:14 2022

@author: sam
"""

import esdbotsecrets
from geopy import Nominatim
import requests
import datetime

    
def esdtest():
    query="York, PA"
    gl = Nominatim(user_agent="ESDBot")
    location = gl.geocode(query)
    url = "https://api.openweathermap.org/data/3.0/onecall?lat={}&lon={}&appid={}".format(location.latitude,location.longitude,esdbotsecrets.OWM_KEY)
    print(url)
    response = requests.get(url)
    print(response.json())
    hum = response.json()["current"]["humidity"]
    if hum >= 30:
        return "The humidity is {}%. The ESD risk is low. Go ahead and rub your feet on the carpet.".format(hum)
    else:
        return "The humidity is {}%. The ESD risk is high. Use ESD precautions!".format(hum)
    
def timetest():
    esdday = datetime.datetime(2023,1,9,7,0,0,0)
    today = datetime.datetime.now()
    delta = today - esdday
    esddays = delta.days
    print(esddays)