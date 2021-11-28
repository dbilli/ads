import sys
import requests
import json
import pprint

import time
import datetime

DEFAULT_URL = 'http://127.0.0.1:4013/exec_pipeline'

args = sys.argv[1:]

filename = args[0]

if len(args) > 1:
    url = args[1]
else:
    url = DEFAULT_URL





steps = [
    {'step1': { 'adtk.transformer.ClassicSeasonalDecomposition': { 'trend': False } } },
    {'step2': { 'adtk.detector.SeasonalAD'                     : { } } },
]







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
    'serie': serie_data,
    'steps': steps,
    'image_file': '/tmp/mygraph.png'
}
resp = requests.post(url, json=serie)

print(resp.text)
result = json.loads(resp.text)

for step_name, step_data in result['steps_results'].items():
    print(step_name)

