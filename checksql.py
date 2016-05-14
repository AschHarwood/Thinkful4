import requests
from pandas.io.json import json_normalize
import pandas as pd 
import collections
import datetime

#r = requests.get('http://www.citibikenyc.com/stations/json')

#df = json_normalize(r.json()['stationBeanList'])

import sqlite3 as lite

con = lite.connect('citi_bike.db')
cur = con.cursor()

citibikesdf = pd.read_sql('SELECT * FROM available_bikes ORDER BY execution_time', con, index_col='execution_time')
#print citibikesdf

hour_change = collections.defaultdict(int)
for col in citibikesdf.columns:
    station_vals = citibikesdf[col].tolist()
    station_id = col[1:] #trim the "_"
    station_change = 0
    for k,v in enumerate(station_vals):
        if k < len(station_vals) - 1:
            station_change += abs(station_vals[k] - station_vals[k+1])
    hour_change[int(station_id)] = station_change #convert the station id back to integer

def keywiththemaxval(d):
	return max(d, key=lambda k: d[k])

max_station = keywiththemaxval(hour_change)
#print max_station

cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
data = cur.fetchone()
print data

print("The most active station is station id %s at %s latitude: %s longitude: %s " % data)
print("With %d bicycles coming and going in the hour between %s and %s" % (
    hour_change[max_station],
    datetime.datetime.fromtimestamp(int(citibikesdf.index[0])).strftime('%Y-%m-%dT%H:%M:%S'),
    datetime.datetime.fromtimestamp(int(citibikesdf.index[-1])).strftime('%Y-%m-%dT%H:%M:%S'),
))
#print hour_change

import matplotlib.pyplot as plt 

plt.bar(hour_change.keys(), hour_change.values())
plt.show()