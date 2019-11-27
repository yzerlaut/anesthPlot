#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 16:05:29 2019

@author: cdesbois
"""
import numpy as np
import pandas as pd

def clean_trenddata(df):

    paramList = ['ip1s','ip1d','ip1m','ip1PR',
                 'co2insp','co2exp','co2RR',
                 'o2insp','o2exp',
                 'aaInsp','aaExp',
                 'pPeak','peep','pPlat',
                 'tvInsp','tvExp','compli','ipeep','pmean','raw',
                 'minVinsp','minVexp','epeep','ieRat',
                 'inspT','expT','peepe','peepi']
    paramsRange = {
            'ip1s' : (30,None),
            'ip1d' : (10,None),
            'ip1m' : (20,None),
            'ip1PR' : (20,80),
            'co2insp' : (None,None),
            'co2exp' : (20,None),
            'co2RR' : (None,None),
            'o2insp' : (None,None),
            'o2exp' : (None,None),
            'aaInsp' : (None,None),
            'aaExp' : (None,None),
            'pPeak' : (None,None),
            'peep' : (None,None),
            'pPlat' : (None,None),
            'tvInsp' : (None,None),
            'tvExp' : (None,None),
            'compli' : (None,None),
            'ipeep' : (None,None),
            'pmean' : (None,None),
            'raw' : (None,None),
            'minVinsp' : (None,None),
            'minVexp' : (None,None),
            'epeep' : (None,None),
            'ieRat' : (None,None),
            'inspT' : (None,None),
            'expT' : (None,None),
            'peepe' : (None,None),
            'peepi' : (None,None)
            }
    # irrelevant
    for item in paramsRange.keys():
        if item in df.columns:
            df.loc[df[item] < paramsRange[item][0], item] = np.NaN
            df.loc[df[item] > paramsRange[item][1], item] = np.NaN
    # outliers
    for item in paramList: 
        if item in df.columns:
            mini, maxi = df[item].quantile([0.01, 0.99])        
            df.loc[df[item] < mini, item] = np.NaN
            df.loc[df[item] > maxi, item] = np.NaN

    #fill with interpolation            
    df = df.interpolate(method='linear')
    #TODO = pb when the animal is disconnected :
    # the linear interpolation is not relevant
    return df