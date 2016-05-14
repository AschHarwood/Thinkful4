import requests
from pandas.io.json import json_normalize
import pandas as pd 

r = requests.get('http://www.citibikenyc.com/stations/json')

df = json_normalize(r.json()['stationBeanList'])

import sqlite3 as lite

con = lite.connect('citi_bike.db')
cur = con.cursor()

# a package for parsing a string into a Python datetime object
from dateutil.parser import parse 

import collections


#take the string and parse it into a Python datetime object
exec_time = parse(r.json()['executionTime'])

import sched
import time
s = sched.scheduler(time.time, time.sleep)

def available_bike_update():
	with con:
	    cur.execute('INSERT INTO available_bikes (execution_time) VALUES (?)', (exec_time.strftime('%s'),))



	id_bikes = collections.defaultdict(int) #defaultdict to store available bikes by station

	#loop through the stations in the station list
	for station in r.json()['stationBeanList']:
	    id_bikes[station['id']] = station['availableBikes']

	#iterate through the defaultdict to update the values in the database
	with con:
	    for k, v in id_bikes.iteritems():
	        cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")

#citibikesdf = pd.read_sql('SELECT * FROM available_bikes', con)
#print citibikesdf

def print_some_time():
	runtime = 0
	while runtime < 60:
		s.enter(60, 1, available_bike_update, ())
		s.run()
		runtime +=1

print_some_time()	

