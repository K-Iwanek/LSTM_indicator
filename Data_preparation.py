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

SEQ_LEN = 1400    #How long of a preceeding sequence to collect for RNN 
FASTEMA=10    #Technical indicator, EMA. We will look for FASTEMA and SLOWEMA crosses. 
SLOWEMA=44    #Technical indicator, EMA. When FASTEMA line is greater than SLOWEMA line we are are looking for local max.
LEARN_DATA=0.90 #Which part of data is learning data. The rest of the data will be used for testing

####Loading the data####
df=pd.read_csv('EURUSD_H1.csv', sep="\t")    #Downloaded from https://data.forexsb.com/data-app#


####FASTEMA and SLOWEMA calculation 
df["FASTEMA"] = ta.ema(df["Close"], length=FASTEMA)
df["SLOWEMA"] = ta.ema(df["Close"], length=SLOWEMA)


#### Dropping Nans
df=df.dropna()
df.reset_index(drop=True, inplace=True)


