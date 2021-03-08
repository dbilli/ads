
import os
import sys

from flask import Flask
from flask import request
from flask import render_template_string
from flask import jsonify

import ads
from ads.api import detect_anomalies

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

# command line parameters  by uWSGI
ARGS = sys.argv

# Environment by uWSGI
GLOBAL_CONTEXT = {
    'VERSION': ads.__version__,
    'APP_ARGS': ARGS,
    
    'CONFIG_LISTEN_ADDRESS': os.environ['CONFIG_LISTEN_ADDRESS'],
    'CONFIG_DATA_DIR'      : os.environ['CONFIG_DATA_DIR'],
    
    'ENVIRON' : os.environ, #[ (k,v) for k,v in os.environ ] ,
}


#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

app = Flask(__name__)

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

@app.route('/')
def index():

    html = '''
<h1>Anomaaly Detection Server {{VERSION}}</h1>
'''
    html = render_template_string(html, **GLOBAL_CONTEXT)

    return html

#----------------------------------------------------------------------#

@app.route('/debug')
def debug():

    html = '''

<h1>Anomaly Detection Server {{VERSION}}</h1>

<h3>CONFIG</h3>

<pre>
CONFIG_LISTEN_ADDRESS = {{ CONFIG_LISTEN_ADDRESS }}
CONFIG_DATA_DIR       = {{ CONFIG_DATA_DIR }}
</pre>


<h3>Environment</h3>

<pre>
{% for k,v in ENVIRON.items() %}
    {{k}} = {{v}}
{% endfor %}
</pre>
'''

    html = render_template_string(html, **GLOBAL_CONTEXT)
    
    return  html

#----------------------------------------------------------------------#

@app.route('/status')
def status():

    response = { 'status': 'running' }

    return jsonify(response)

#----------------------------------------------------------------------#

@app.route('/detect', methods=['POST'])
def detect():

    if request.method != 'POST':
        return 'NO POST'
        
    request_obj = request.json
    
    serie_data = request_obj['serie']

    anomalies = detect_anomalies(serie_data)

    response = {
        'anomalies': anomalies
    }
    return jsonify(response)
