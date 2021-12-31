'''
FORMAT 1
==============================

YAML

- step1:
    adtk.transformer.ClassicSeasonalDecomposition:
      trend: false
- step2:
    adtk.detector.SeasonalAD: {}

JSON

[
    {'step1': { 'adtk.transformer.ClassicSeasonalDecomposition': { 'trend': False } } },
    {'step2': { 'adtk.detector.SeasonalAD'                     : { } } },
]

FORMAT 2
==============================

YAML

- - step1
  - adtk.transformer.ClassicSeasonalDecomposition:
      trend: true
- - step2
  - adtk.detector.SeasonalAD: {}


JSON

[
    [ 'step1', { 'adtk.transformer.ClassicSeasonalDecomposition': { 'trend': True } } ],
    [ 'step2', { 'adtk.detector.SeasonalAD'                     : { }               } ],
]


FORMAT 3
==============================

YAML

- - step1
  - - adtk.transformer.ClassicSeasonalDecomposition
    - trend: true
- - step2
  - - adtk.detector.SeasonalAD
    - {}


JSON

[
    [ 'step1', [ 'adtk.transformer.ClassicSeasonalDecomposition', { 'trend': True } ] ],
    [ 'step2', [ 'adtk.detector.SeasonalAD'                     , { }               ] ],
]


FORMAT 4
==============================

YAML

- - step1
  - - adtk.transformer.ClassicSeasonalDecomposition
    - - - trend
        - true
- - step2
  - - adtk.detector.SeasonalAD
    - []

JSON

[
    [ 'step1', [ 'adtk.transformer.ClassicSeasonalDecomposition', [ ['trend', True] ] ] ],
    [ 'step2', [ 'adtk.detector.SeasonalAD'                     , [                 ] ] ],
]
document = yaml.dump(steps)
print(document)
'''

import sys
import time
import datetime
import pandas as pd

#import adtk.detector 
#from adtk.detector import SeasonalAD

from adtk.data import validate_series
from adtk.pipe import Pipeline

from adtk.visualization import plot

import matplotlib.pyplot as plt

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

def _mangle_serie_data(serie_data, step=60):

    index = []
    data  = []
    for t,v in serie_data:
        index.append( pd.to_datetime(t, unit='s') )
        data.append(v)
    s_train = pd.Series(index=index, data=data)
    s_train = s_train.resample( pd.Timedelta(seconds=step) ) 
    s_train = s_train.pad()
    s_train = validate_series(s_train)
    return s_train

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#

#def detect_anomalies(serie_data):
#
#    s_train = _mangle_serie_data(serie_data)
#    
#    d = SeasonalAD()
#    anomalies = d.fit_detect(s_train) #, return_list=True)
#    
#    #d = adtk.detector.InterQuartileRangeAD() #low=300, high=28000)
#    #anomalies = d.fit(s_train)
#    #anomalies = d.detect(s_train)    
#    
#    anomalies = anomalies.reset_index().values.tolist()
#
#    # Converti index timestamp to float
#    for r in anomalies:
#        r[0] = r[0].timestamp()
#
#    return anomalies

#----------------------------------------------------------------------#
#                                                                      #
#----------------------------------------------------------------------#


def __load_symbol( module_full_symbol_name ):

        module_fullname, symbol = module_full_symbol_name.rsplit('.', 1)
        
        # Load module (dlopen())
        try:
                mod = __import__(module_fullname, {}, {}, [symbol])
        except ImportError as e:
                raise Exception('Error importing handler %s: "%s"' % (module_fullname, e))
        except ValueError as e:
                raise Exception('Error importing handler! Invalid Value: %s' % (e))
        # get symbol (dlsym())
        try:
                var = getattr(mod, symbol)
        except AttributeError:
                raise Exception('Module "%s" does not define a "%s" table! ' % (module_fullname, symbol))
        return var



def load_pipeline(steps):

    def _load_step(step):

        if isinstance(step, dict):
            step = list(step.items())[0]

        name, conf = step
        
        if isinstance(conf, dict):
            conf = list(conf.items())[0]

        symbol, params = conf
            
        klass = __load_symbol(symbol)
        
        params = params or {}
        
        if isinstance(params, list):
            params = dict(params)
        
        obj = klass(**params)
        
        return (name, obj)

    obj = [ _load_step(s) for s in steps ]
    
    return Pipeline(obj)


def create_image(image_file, pipeline_result):
    SIZE=5000
    plot_def = {}
    for k, v in pipeline_result.items(): 
        data        = pipeline_result[k]
        plot_def[k] = data[-SIZE:]
    
    plot_result = pd.DataFrame( plot_def ) 
    plot(plot_result)
    plt.savefig(image_file) 
        
        
def execute_pipeline(steps, serie_data, image_file=None, data_step=60):

    s_train = _mangle_serie_data(serie_data, step=data_step)

    # EXECUTE
    pipeline = load_pipeline(steps)
    pipeline_result = pipeline.fit_detect(s_train, return_intermediate=True)
    
    
    if image_file:
        create_image(image_file, pipeline_result)

    result = {}
    for name, serie in pipeline_result.items(): 
        serie_data = serie.reset_index().values.tolist()

        # Converti index timestamp to float
        for row in serie_data:
            row[0] = row[0].timestamp()
    
        result[name] = serie_data

    return result
