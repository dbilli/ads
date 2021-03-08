import sys
import requests
import json
import pprint

import time
import datetime

DEFAULT_URL = 'http://127.0.0.1:4013/detect'

args = sys.argv[1:]

filename = args[0]

if len(args) > 1:
    url = args[1]
else:
    url = DEFAULT_URL

#
# Load
#
serie_data = []

f = open(filename, "r") 
lines = f.readlines()
for r in lines[1:]:
    t,v = r.strip().split(',')
    try:
        t = time.mktime(datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S").timetuple())
    except Exception as e:
        t = int(t)
    serie_data.append( (t,int(v)) )
f.close()

#
# Send/receive
#
serie = {
    'serie': serie_data
}
resp = requests.post(url, json=serie)

print(resp.text)
#pprint.pprint(json.loads(resp.text))

