# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 18:27:48 2022

@author: Krzychu
"""


import pandas as pd
import numpy as np
import pandas_ta as ta
from collections import deque
import random


####Variables####

SEQ_LEN = 1400    # How long of a preceeding sequence to collect for RNN 
FASTEMA=10    # Technical indicator, EMA. We will look for FASTEMA and SLOWEMA crosses. 
SLOWEMA=44    # Technical indicator, EMA. When FASTEMA line is greater than SLOWEMA line we are are looking for local max.
LEARN_DATA=0.90 # Which part of data is learning data. The rest of the data will be used for testing

#### Loading the data ####
df=pd.read_csv('EURUSD_H1.csv', sep="\t")    # Downloaded from https://data.forexsb.com/data-app#


####FASTEMA and SLOWEMA calculation 
df["Fastema"] = ta.ema(df["Close"], length=FASTEMA)
df["Slowema"] = ta.ema(df["Close"], length=SLOWEMA)


#### Dropping Nans ####
df.dropna()
df.reset_index(drop=True, inplace=True)


#### Searching for trend ####
df['Trend'] = np.where(df['Fastema']>df['Slowema'], 1, 0)
df['Trend-1']=df['Trend'].shift(periods=1)
df["Trend_Change"]=df['Trend']-df['Trend-1']  # When Fastema starts to be smaller than Slowema: Trend_Change = -1. When greater: Trend_Change = 1

#### Makeing list of interval's starts
interval=df.index[df['Trend_Change'] != 0].tolist()  
interval.pop(0) # 1st element is Na

#### Searching for local Max and Minimus ####
df["Max"]=np.nan       
df['Min']=np.nan 


if df['Trend_Change'][interval[0]]==1: # We are checking, our data is starting at rising or downward trend
    start=1 # Rising trend
else:
    start=0 # Downward trend

    
for i in range(0,len(interval)-1):  #Supplement Min and Max cols in intervals
    if i%2==start:
        minimums=df['Close'][interval[i]:interval[i+1]] 
        
        df["Min"][interval[i]:interval[i+1]]=min(minimums)
    else:
        maximus=df['Close'][interval[i]:interval[i+1]]    
      
        df["Max"][interval[i]:interval[i+1]]=max(maximus)
  
        
df['Local_Max']=np.where(df['Max']==df['Close'], df['Close'],0) # Says, when we have local Max
df['Local_Min']=np.where(df['Min']==df['Close'], df['Close'],0) # Says, when we have local Min
df['Extreme']=df['Local_Max']+df['Local_Min'] 


#### Clearing beginning of the data ####
extrems=df.index[df['Extreme'] != 0].tolist() # List of extrems
df.drop(df.index[0:extrems[0]], inplace=True) #drop rows, where we dont know extrems


#### Index reset and update of the extrems list ####
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

extrems=df.index[df['extremum'] != 0].tolist()



        
        
        
        