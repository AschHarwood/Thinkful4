import requests
import sqlite3 as lite
import datetime

api_key = "<api_key>"
url = 'https://api.forecast.io/forecast/' + api_key

cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }