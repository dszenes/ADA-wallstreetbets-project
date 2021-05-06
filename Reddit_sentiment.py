import praw
import json
import datetime as dt
from datetime import datetime, timedelta
from psaw import PushshiftAPI 
import pandas as pd
import numpy as np
import math

api = PushshiftAPI()



    

    
def scraping_oneday(day,n) :
    day=dt.datetime.strptime(day, "%d-%m-%Y")
    end_date = day + dt.timedelta(days=1)
    return(list(api.search_submissions(after=day,before=end_date,subreddit='wallstreetbets',q='GME',filter=['selftext','title','score','num_comments'],limit=n)))
    

    
    
    
    
    
    
    
    
def scraping_multipleday(start_day,end_day,n) :
    
    start_date=dt.datetime.strptime(start_day, "%d-%m-%Y")     #getting the list of all dates we are interested to
    end_date=dt.datetime.strptime(end_day, "%d-%m-%Y")
    delta = end_date - start_date       # as timedelta
    list_date=[]
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        list_date.append(day)
        
    list_post=[] 
    for DAY in list_date :
        list_post.append(scraping_oneday(DAY.strftime("%d-%m-%Y"),n))
    return(list_post)



m2=scraping_multipleday("01-01-2021","30-01-2021",5000)



    
    
def cleen_df(scrap_multiple,start_day,end_day) :
    df=pd.DataFrame()                             #In this function i get the submissions of all the day and return a cleen dataframe 
    array_scrap=np.array(scrap_multiple)
    list_date=[]
    label_row=['Total sub','Total Comments','Total Score','All content', 'All titles']
    start_date=dt.datetime.strptime(start_day, "%d-%m-%Y")     #getting the list of all dates we are interested to
    end_date=dt.datetime.strptime(end_day, "%d-%m-%Y")
    delta = end_date - start_date                                   #Create a list of all the dates concerned about our study
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        list_date.append(day)
    df=df.reindex(list_date)
    df=df.reindex(label_row,axis=1)
    nb_param=7
    
    for day in range (len(scrap_multiple)) :
        for param in range(len(scrap_multiple[day])) :
            if(param==0):
                df.iloc[day,0]=len(scrap_multiple[day])
                df.iloc[day,1]=0
                df.iloc[day,2]=0
                df.iloc[day,3]=""
                df.iloc[day,4]=""
            df.iloc[day,1]+=scrap_multiple[day][param][1]
            df.iloc[day,2]+=scrap_multiple[day][param][2]
            if((len(scrap_multiple[day][param])==nb_param)) :               #add the content of the submission only if it exists (since some posts have only a title and no content)
                if((scrap_multiple[day][param][3]!=('[removed]'))and(scrap_multiple[day][param][3]!=('[deleted]'))) :
                    
                    df.iloc[day,3]+=str(scrap_multiple[day][param][3])+' '
                df.iloc[day,4]+=scrap_multiple[day][param][4]+' '
            else :
                df.iloc[day,4]+=scrap_multiple[day][param][3]+' '
    return(df)

m3=cleen_df(m2,'01-01-2021','30-01-2021')
m3.index.names=['Date']
        



#Code Richard

import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader.data as web

%matplotlib inline


# Get data from yahoo finance
# Historical stock price 
gme = yf.download('GME','2020-01-01','2021-01-30')


# Compute Daily Volatility
# First let's compute the daily return
gme['Log_Ret'] = np.log(gme['Close'] / gme['Close'].shift(1))

# Compute Volatility using the pandas rolling standard deviation function
wtd = 5 #window of trading days
gme['Volatility'] = gme['Log_Ret'].rolling(window=wtd).std() * np.sqrt(wtd)

# Plot the Price series and the Volatility
gme[['Close', 'Volatility']].plot(title = 'GameStop', subplots=True,figsize=(8, 8))

gme


#Merge the prices dataframe with the reddit dataframe


merged_df=m3.merge(gme,how='left',on='Date')


#Delete the days with no financial data such as weekends and add the submission of those days to the next trading day.

nb_comm=0
nb_post=0
nb_score=0
all_txt=''
all_titles=''
test=0
DAY=0
while( DAY <merged_df.shape[0]) :
    
    if(DAY>merged_df.shape[0]-1) :
        print('ok')
        break
    
    if(math.isnan(merged_df.iloc[DAY,5])) :
        nb_post+=merged_df.iloc[DAY,0]
        nb_comm+=merged_df.iloc[DAY,1]
        nb_score+=merged_df.iloc[DAY,2]
        all_txt+=str(merged_df.iloc[DAY,3])
        all_titles+=str(merged_df.iloc[DAY,4])
        test=1
        merged_df=merged_df.drop(merged_df.index[DAY],axis=0)
        print(DAY)
        DAY=DAY-1
        
    else :
        if(test==1) :
           merged_df.iloc[DAY,0]+=nb_post
           merged_df.iloc[DAY,1]+=nb_comm
           merged_df.iloc[DAY,2]+=nb_score
           merged_df.iloc[DAY,3]=' '+ all_txt+ str(merged_df.iloc[DAY,3])
           merged_df.iloc[DAY,4]+=' '+ all_titles
           nb_comm=0
           nb_post=0
           nb_score=0
           all_txt=''
           all_titles=''
           test=0
           
    DAY=DAY+1
        
        
  
        
merged_df.to_csv('dataframe2.csv',sep=',')
        
        
    
    
    
    
    
    
    
    
    