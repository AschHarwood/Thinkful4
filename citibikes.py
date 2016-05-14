"""import statements"""

import requests
from pandas.io.json import json_normalize
import time
from dateutil.parser import parse
import collections
import pandas as pd 
import sqlite3 as lite




#download citibike data
r = requests.get('http://www.citibikenyc.com/stations/json')


#get keys from citibikes dict

r.json().keys

#def create_dataframe():
df = json_normalize(r.json()['stationBeanList'])

con = lite.connect('citi_bike2.db')

cur = con.cursor()


key_list = []
for station in r.json()['stationBeanList']:
	for k in station.keys():
		if k not in key_list:
			key_list.append(k)



# SQL Functions


# create_reference_table():

with con:
	cur.execute('DROP TABLE citibike_reference')
	cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT)')


# insert_into_table():
sql = "INSERT INTO citibike_reference(id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

with con:
	for station in r.json()['stationBeanList']:
		cur.execute(sql,(station['id'], station['totalDocks'], station['city'], station['altitude'], station['stAddress2'], station['longitude'], station['postalCode'], station['testStation'], station['stAddress1'], station['stationName'], station['landMark'], station['latitude'], station['location']))

#def create_station_ids():
station_ids = df['id'].tolist()


station_id_strings = ['_' + str(x) + 'INT' for x in station_ids] #creates new column headings out of ids

# create_available_bikes_table():
with con:
	#cur.execute("DROP TABLE available_bikes")
	cur.execute("CREATE TABLE available_bikes ( execution_time INT, " + ", ".join(station_ids) + ");")

exec_time = parse(r.json()['executionTime'])

# insert_into_available_bikes():
with con:
	cur.execute('INSERT INTO available_bikes (execution_time)'' VALUES(?)', (exec_time.strftime('%s'),))

id_bikes = collections.defaultdict(int)

for station in r.json()['stationBeanList']:
	id_bikes[station['id']] = station['availableBikes']

with con:
	for k,v in id_bikes.iteritems():
		cur.execute("UPDATE available_bikes SET _" + str(k) + " = " + str(v) + " WHERE execution_time = " + exec_time.strftime('%s') + ";")












