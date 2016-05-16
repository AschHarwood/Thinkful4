import sqlite3 as lite
import pandas as pd 
import matplotlib.pyplot as plt  

con = lite.connect('weather3.db')
df = pd.read_sql('SELECT * FROM daily_temp', con)

print df 

city_temp_range = df.max() - df.min()
print city_temp_range