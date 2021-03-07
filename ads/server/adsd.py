
import json
import sys
import os

from flask import Flask
from flask import render_template_string


import ads

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

ARGS = sys.argv

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
#                                                                      #
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
#                                                                      #
#----------------------------------------------------------------------#

@app.route('/status')
def status():

    response = { 'status': 'running' }

    response = json.dumps(response)

    return response

