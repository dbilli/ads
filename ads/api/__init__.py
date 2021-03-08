

import pandas as pd

import adtk.detector 
from adtk.detector import SeasonalAD
from adtk.data import validate_series


def detect_anomalies(serie_data):

    index = []
    data  = []
    
    for t,v in serie_data:
        index.append( pd.to_datetime(t, unit='s') )
        data.append(v)
    

    s_train = pd.Series(index=index, data=data)
    
    s_train = s_train.resample("30 min")    
    s_train = s_train.pad()
    s_train = validate_series(s_train)
    
    d = SeasonalAD()
    anomalies = d.fit_detect(s_train) #, return_list=True)
    
    #d = adtk.detector.InterQuartileRangeAD() #low=300, high=28000)
    #anomalies = d.fit(s_train)
    #anomalies = d.detect(s_train)    
    
    anomalies = anomalies.reset_index().values.tolist()

    # Converti index timestamp to float
    for r in anomalies:
        r[0] = r[0].timestamp()

    return anomalies
