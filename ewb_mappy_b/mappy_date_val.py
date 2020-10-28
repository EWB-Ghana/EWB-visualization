#!/usr/bin/env python3

from datetime import timedelta, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
Paramenters: df of map layer data 
Will convert values in mm/dd/YYYY, mm/dd/yy, mm-dd-YYYY, mm-dd-yy string to dt
Will also accept dates that are already in the datetime type
If date is in incorrect format, will print out an error message
returns a copy of the map dataframe, with added columns that have the date in proper datetime and date format
original df remains unchanged





''''
def date_val(df):
    df_copy =df.loc[:]
    
    df_len = len(df_copy)
    df_copy['Date_str']=pd.Series(['']*df_len)
    df_copy['Date_dt']= pd.Series(['']*df_len)
    for i in range (len(df_copy)):
        date = df_copy.Date.iloc[i]
        date_dt =0
        date_str=''
        if type (date)== datetime:
            date_dt =date
            date_str = '{}/{}/{}'.format(date_dt.month,date_dt.day, date_dt.year)
        elif type(date)== str:
            try:
                if '/' in date:
                    date_split =date.split('/')
                    #if the 'year' is written fully
                    if len (date_split[-1])== 4:
                        date_dt = datetime.strptime(date,'%m/%d/%Y')
                    #if 'year' is only last two digits of year
                    else:
                        date_dt = datetime.strptime(date,'%m/%d/%y')
                    date_str = '{}/{}/{}'.format(date_dt.month,date_dt.day, date_dt.year)
                elif '-' in date:
                    date_split =date.split('-')
                    #if the 'year' is written fully
                    if len (date_split[-1])== 4:
                        date_dt = datetime.strptime(date,'%m-%d-%Y')
                    #if 'year' is only last two digits of year
                    else:
                        date_dt = datetime.strptime(date,'%m/%d/%y')
                    date_dt = datetime.strptime(date,'%m-%d-%Y')
                    date_str = '{}/{}/{}'.format(date_dt.month,date_dt.day, date_dt.year)
            except:
                #improper dt format
                print ("'{}' is not in an acceptable date format".format(date))
        df_copy['Date_str'].iloc[i] =date_str
        df_copy['Date_dt'].iloc[i] =date_dt
    return df_copy
        
