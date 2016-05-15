
import sqlite3 as lite
import datetime
import requests
from pandas.io.json import json_normalize
import time
from dateutil.parser import parse 
import collections
import pandas as pd

con = lite.connect('citi_bike.db')
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM available_bikes ORDER BY execution_time",con,index_col='execution_time')

with con:
    cur.execute("SELECT max(execution_time) FROM available_bikes")
    
rows = cur.fetchall()
mx = rows[0][0]

with con:
    cur.execute("SELECT min(execution_time) FROM available_bikes")
rows = cur.fetchall()
mn = rows[0][0] 
mxchg = 0
chgarray = []
for a in df.columns:
    s = df[a]
    chg = abs(s[mx] - s[mn])
    s1 = chg.tolist()
    s2 = s1[0]
    chgarray.append([a,s2])
    if s2 > mxchg:
        mxchg = s2
        mxrw = a

#query sqlite for reference information
max_station = a[1:]

with con:
    cur.execute("SELECT id, stationname, latitude, longitude FROM citibike_reference WHERE id = ?", (max_station,))
    data = cur.fetchone()

print "The most active station is station id %s at %s latitude: %s longitude: %s " % data
print "With " + str(mxchg) + " bicycles coming and going in the hour between " + datetime.datetime.fromtimestamp(int(df.index[0])).strftime('%Y-%m-%dT%H:%M:%S') + " and " + datetime.datetime.fromtimestamp(int(df.index[-1])).strftime('%Y-%m-%dT%H:%M:%S')