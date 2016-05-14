import requests
from pandas.io.json import json_normalize
import pandas as pd 

r = requests.get('http://www.citibikenyc.com/stations/json')

df = json_normalize(r.json()['stationBeanList'])

import sqlite3 as lite

con = lite.connect('citi_bike.db')
cur = con.cursor()

citibikesdf = pd.read_sql('SELECT * FROM available_bikes', con)
print citibikesdf