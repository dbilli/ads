
import os
import sys
import traceback
import datetime
import copy
import urllib

from flask import Flask
from flask import request
from flask import render_template_string
from flask import jsonify
from flask import url_for

from werkzeug.exceptions import HTTPException

import ads
from ads.api import execute_pipeline

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

# command line parameters  by uWSGI
ARGS = sys.argv

# Environment by uWSGI
GLOBAL_CONTEXT = {
    'VERSION'              : ads.__version__,
    'APP_ARGS'             : ARGS,
    
    'CONFIG_LISTEN_ADDRESS': os.environ['CONFIG_LISTEN_ADDRESS'],
    'CONFIG_DATA_DIR'      : os.environ['CONFIG_DATA_DIR'],
    'CONFIG_DEBUG_MODE'    : os.environ['CONFIG_DEBUG_MODE'],
    
    'ENVIRON'              : os.environ, #[ (k,v) for k,v in os.environ ] ,
    
    'start_time'           : datetime.datetime.now()
}

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

app = Flask(__name__, 
    static_folder=None,  # disable /static 
)

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

@app.route('/')
def index():
    """
    """
        
    html = '''
<h1>Anomaly Detection Server (v{{VERSION}}) </h1>

Uptime: {{uptime}} (started at {{start_time}})
'''

    context = copy.copy(GLOBAL_CONTEXT)

    context['uptime'] = datetime.datetime.now() - context['start_time']

    html = render_template_string(html, **context)

    return html

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

@app.route('/debug')
def debug():
    """
    """

    if not GLOBAL_CONTEXT['CONFIG_DEBUG_MODE']:
        return 'Debug mode not enabled', 404


    html = '''

<h1>Anomaly Detection Server {{VERSION}}</h1>

<h3>URLS</h3>

{% for line in URLS|sort %}    
<pre style="background-color:#f0f0f0">
{{line}}
</pre>
{% endfor %}

<h3>Config</h3>

<pre>
CONFIG_LISTEN_ADDRESS = {{ CONFIG_LISTEN_ADDRESS }}
CONFIG_DATA_DIR       = {{ CONFIG_DATA_DIR }}
</pre>


<h3>Environment</h3>

<pre>
{% for k,v in ENVIRON.items()|sort %}{{k}} = {{v}}
{% endfor %}
</pre>
'''
    urls = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        #line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        line = urllib.parse.unquote("{:20s} {}".format(methods, url))
        urls.append(line)
        
        
    context = copy.copy(GLOBAL_CONTEXT)
    
    context['URLS'] = urls

    html = render_template_string(html, **context)
    
    return  html

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

#@app.route('/status')
#def status():
#
#    response = { 'status': 'running' }
#
#    return jsonify(response)

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

@app.route('/exec_pipeline', methods=['POST'])
def exec_pipeline():
    """
    """

    try:
        if request.method != 'POST':
            return 'NO POST'
    
        #
        # 
        #
        request_obj = request.json
        
        serie_data = request_obj['serie']
        steps      = request_obj['steps']
        image_file = request_obj.get('image_file')
        data_step  = request_obj.get('data_step', 60)
    
        #
        # Process
        #     
        steps_result = execute_pipeline(steps, serie_data, image_file=image_file, data_step=data_step)
    
        #
        # Response
        #
        response = {
            'steps_results': steps_result
        }
    
        return jsonify(response)

    except Exception as e:

        msg = "Generic error: %s" % (e)
        return msg, 500


#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

#@app.route('/detect', methods=['POST'])
#def detect():
#
#    if request.method != 'POST':
#        return 'NO POST'
#        
#    request_obj = request.json
#    
#    serie_data = request_obj['serie']
#
#    anomalies = detect_anomalies(serie_data)
#
#    response = {
#        'anomalies': anomalies
#    }
#    return jsonify(response)
