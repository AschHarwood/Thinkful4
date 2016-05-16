import requests
import datetime
import time
import pandas as pd 
from pandas.io.json import json_normalize
import sqlite3 as lite

start_date = datetime.datetime.now() - datetime.timedelta(days=30)
start_datestr = start_date.strftime('%s')
#start_date = start_date.strftime('%s')
#start_date = time.mktime(start_date.timetuple())
#date is not working in cod
#cities_weather = requests.get('https://api.forecast.io/forecast/e967d7c3d78c3979655d077839f5c60c/40.680991,-73.998259') 
#print cities_weather.status_code
#print cities_weather.json().keys()
#df = json_normalize(cities_weather.json()['hourly'])
#dailymaxtemp = max(df)

"""need to create sql database and table"""
con = lite.connect('weather.db')
cur = con.cursor()

with con:
	cur.execute("DROP TABLE IF EXISTS daily_max_temp")
	con.execute('CREATE TABLE daily_max_temp (daytime TEXT, city1 REAL, city2 REAL, city3 REAL, city4 REAL, city5 REAL)')

"""loop to iterate days"""

cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }
dayweather = 0
for dayweather in range(30):
	for city in cities.values():
		cities_weather = requests.get('https://api.forecast.io/forecast/e967d7c3d78c3979655d077839f5c60c/%s, %s' % (city, start_datestr))
		df = json_normalize(cities_weather.json()['hourly']['data']) #need to set index as time
		df_indexed= df.set_index(df['time'])
		dailymaxtemp = max(df_indexed['temperature'])
		dailymaxtempidx=df_indexed['temperature'].idxmax()
	with con:
			cur.execute('INSERT INTO daily_max_temp(daytime, dailymaxtemp) VALUES (?,?)', (dailymaxtempidx, city))
	#insert SQL update statement here that grabs 
	dayweather += 1
	start_date = start_date + datetime.timedelta(days=1)
	start_datestr = start_date.strftime('%s')

df = pd.read_sql('SELECT * FROM daily_max_temp', con)

print df 







