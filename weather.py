import requests
import datetime
import time
import pandas as pd 
from pandas.io.json import json_normalize

start_date = datetime.datetime.now() - datetime.timedelta(days=30)
#start_date = start_date.strftime('%s')


#start_date = time.mktime(start_date.timetuple())


#date is not working in cod
cities_weather = requests.get('https://api.forecast.io/forecast/e967d7c3d78c3979655d077839f5c60c/40.680991,-73.998259') 
print cities_weather.status_code

#print cities_weather.json().keys()

df = json_normalize(cities_weather.json()['hourly'])
dailymaxtemp = max(df)

"""need to create sql database and table"""
#insert code here

"""loop to iterate days"""

dayweather = start_date
while dayweather != datetime.datetime.now():
	cities_weather = requests.get('https://api.forecast.io/forecast/e967d7c3d78c3979655d077839f5c60c/40.680991,-73.998259, %s' % dayweather) 
	df = json_normalize(cities_weather.json()['hourly'])
	dailymaxtemp = max(df)
	#insert SQL update statement here that grabs 
	dayweather = start_date + datetime.timedelta(days=1)