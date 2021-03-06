#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 24 13:43:26 2019

@author: cdesbois
"""
import os
import pandas as pd
#import numpy as np
from PyQt5.QtWidgets import QFileDialog

#%%
def gui_choosefile(paths, direct=None):
    """ Select a file via a dialog and return the file name. """
    if not direct:
        direct = paths['data']
    fname = QFileDialog.getOpenFileName(caption='choose a file',
                                        directory=direct, filter='*.csv')
    return fname[0]

#%% Monitor trend
def loadmonitor_trendheader(datafile):
    """ extract the header and return a dictionary """
    df = pd.read_csv(datafile, sep=',', header=None, index_col=None,
                     nrows=11, encoding='iso8859_15')
    #NB encoding needed for accentuated letters
    df = df.set_index(0).T
    # convert to num
    df.Weight = df.Weight.astype(float)
    df.Height = df.Height.astype(float)
    df['Sampling Rate'] = df['Sampling Rate'].astype(float)
    # convert to a dictionary
    descr = df.loc[1].to_dict()
    return descr

def loadmonitor_trenddata(datafile, header):
    """ load the monitor trend data, return a pandasDataframe """
    try:
        df = pd.read_csv(datafile, sep=',', skiprows=[13], header=12)
    except:
        df = pd.read_csv(datafile, sep=',', skiprows=[13], header=12,
                         encoding="ISO-8859-1")
    if len(df) == 0:
        print('no recorded values in this file', datafile.split('/')[-1])
        return df
    #remove waves time indicators (column name beginning with a '~')
    for col in df.columns:
        if col[0] == '~':
            del df[col]
    to_fix = []
    for col in df.columns:
        if df[col].dtype != 'float64':
            if col != 'Time':
                to_fix.append(col)
    for col in to_fix:
#        print (col, '\t dtype is', data[col].dtype)
        df[col] = pd.to_numeric(df[col], errors='coerce')
#        print ('after')
#        print (col, '\t dtype is', data[col].dtype)

    #elapsed time (in seconds)
    df['eTime'] = df.index * header['Sampling Rate']
    df['eTimeMin'] = df.eTime/60

    # correct the titles
    corr_title = {'AA  LB': 'aaLabel', 'AA_Insp':'aaInsp', 'AA_Exp':'aaExp',
                  'CO2 RR': 'co2RR', 'CO2_Insp': 'co2insp', 'CO2_Exp' : 'co2exp',
                  'ECG HR': 'ekgHR',
                  'IP1_M' : 'ip1m', 'IP1_S' : 'ip1s', 'IP1_D' : 'ip1d',
                  'IP1PR' : 'hr',
                  'IP2_M' : 'ip2m', 'IP2_S' : 'ip2s', 'IP2_D' : 'ip2d',
                  'IP2PR' : 'ip2PR',
                  'O2_Insp' : 'o2insp', 'O2_Exp' : 'o2exp',
                  'Time'   : 'datetime',
                  'Resp': 'resp',
                  'PPeak': 'pPeak', 'Peep' : 'peep', 'PPlat': 'pPlat', 'pmean':'pmean',
                  'ipeep':'ipeep',
                  'TV_Insp': 'tvInsp', 'TV_Exp' : 'tvExp',
                  'Compli': 'compli',
                  'raw': 'raw',
                  'MinV_Insp': 'minVinsp', 'MinV_Exp': 'minVexp',
                  'epeep': 'epeep', 'peepe': 'peepe', 'peepi': 'peepi',
                  'I:E': 'ieRat', 'Inp_T': 'inspT', 'Exp_T': 'expT', 'eTime': 'eTime',
                  'S_comp': 'sCompl', 'Spplat': 'sPplat'}
    df.rename(columns=corr_title, inplace=True)

#TODO : implement aalabel decoding (4 = iso, 6 = sevo ... and adjust the plot functions

    # remove empty rows and columns
    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)

    # remove comments present in colon 1(ie suppres if less than 5 item rows)
    df = df.dropna(thresh=6)
    # should be interesting to export the comment

    # CO2: from % to mmHg
    try:
        df[['co2exp', 'co2insp']] *= 760/100
    except:
        print('no capnographic recording')

    # convert time to dateTime
    df.datetime = df.datetime.apply(lambda x: header['Date'] + '-' + x)
    df.datetime = pd.to_datetime(df.datetime, format='%d-%m-%Y-%H:%M:%S')

    # remove irrelevant measures
    #df.co2exp.loc[data.co2exp < 30] = np.nan
    #TODO : find a way to proceed without the error pandas displays

    return df


if __name__ == '__main__':
    fileName = gui_choosefile(paths={'data':'~'})
    file = os.path.basename(fileName)
    if file[0] == 'M':
        if 'Wave' not in file:
            header = loadmonitor_trendheader(fileName)
            mdata = loadmonitor_trenddata(fileName, header)
            #mdata= cleanMonitorTrendData(mdata)
            