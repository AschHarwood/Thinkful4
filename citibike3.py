import sqlite3 as lite
import datetime
import requests
from pandas.io.json import json_normalize
import time
from dateutil.parser import parse 
import collections
import pandas as pd


r = requests.get('http://www.citibikenyc.com/stations/json')
df = json_normalize(r.json()['stationBeanList'])

con = lite.connect('citi_bike7.db')
cur = con.cursor()

#load static data about bike stations
with con:
  cur.execute('DROP TABLE IF EXISTS citibike_reference')
  cur.execute('CREATE TABLE citibike_reference (id INT PRIMARY KEY, totalDocks INT, city TEXT, altitude INT, stAddress2 TEXT, longitude NUMERIC, postalCode TEXT, testStation TEXT, stAddress1 TEXT, stationName TEXT, landMark TEXT, latitude NUMERIC, location TEXT )')
#a prepared SQL statement we're going to execute over and over again
sql = "INSERT INTO citibike_reference (id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"

with con:
  for station in r.json()['stationBeanList']:
  #id, totalDocks, city, altitude, stAddress2, longitude, postalCode, testStation, stAddress1, stationName, landMark, latitude, location)
  cur.execute(sql,(station['id'],station['totalDocks'],station['city'],station['altitude'],station['stAddress2'],station['longitude'],station['postalCode'],station['testStation'],station['stAddress1'],station['stationName'],station['landMark'],station['latitude'],station['location']))
#extract the column from the DataFrame and put them into a list
station_ids = df['id'].tolist() 

#add the '_' to the station name and also add the data type for SQLite
station_ids = ('_' + str(x) + ' INT' for x in station_ids) 

#clear bike data with every run of the code
with con:
 cur.execute("DROP TABLE IF EXISTS available_bikes")
 cur.execute("CREATE TABLE available_bikes ( execution_time INT, " + ", ".join(station_ids) + ");")

for a in range(60):
  r = requests.get('http://www.citibik

Enter chat message or link here
