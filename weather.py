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
	con.execute('CREATE TABLE daily_max_temp (daytime TEXT, dailymaxtemp INT)')

"""loop to iterate days"""

dayweather = 0
for dayweather in range(30):
	cities_weather = requests.get('https://api.forecast.io/forecast/e967d7c3d78c3979655d077839f5c60c/40.680991,-73.998259, %s' % start_datestr)
	df = json_normalize(cities_weather.json()['hourly']['data']) #need to set index as time
	df_indexed= df.set_index(df['time'])
	dailymaxtemp = max(df_indexed['temperature'])
	dailymaxtempidx=df_indexed['temperature'].idxmax()
	with con:
		cur.execute('INSERT INTO daily_max_temp(daytime, dailymaxtemp) VALUES (?,?)', (dailymaxtempidx, dailymaxtemp))
	#insert SQL update statement here that grabs 
	dayweather += 1
	start_date = start_date + datetime.timedelta(days=1)
	start_datestr = start_date.strftime('%s')

df = pd.read_sql('SELECT * FROM daily_max_temp', con)

print df 







