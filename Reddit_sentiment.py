import praw
import json
import datetime as dt
from datetime import datetime, timedelta
from psaw import PushshiftAPI 
import pandas as pd
import numpy as np

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



m2=scraping_multipleday("12-01-2021","15-01-2021",10)



    
    
def cleen_df(scrap_multiple,start_day,end_day) :
    df=pd.DataFrame()                             #In this function i get the submissions of all the day and return a cleen dataframe 
    array_scrap=np.array(scrap_multiple)
    list_date=[]
    label_row=['Total Comments','Total Score','All content', 'All titles']
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
        for param in range(nb_param) :
            if(param==0):
                df.iloc[day,0]=0
                df.iloc[day,1]=0
                df.iloc[day,2]=""
                df.iloc[day,3]=""
            df.iloc[day,0]+=scrap_multiple[day][param][1]
            df.iloc[day,1]+=scrap_multiple[day][param][2]
            if((len(scrap_multiple[day][param])==nb_param)) :               #add the content of the submission only if it exists (since some posts have only a title and no content)
                if((scrap_multiple[day][param][3]!=('[removed]'))and(scrap_multiple[day][param][3]!=('[deleted]'))) :
                     df.iloc[day,2]+=str(scrap_multiple[day][param][3])+' '
                df.iloc[day,3]+=scrap_multiple[day][param][4]+' '
            else :
                df.iloc[day,3]+=scrap_multiple[day][param][3]+' '
    return(df)

m3=cleen_df(m2,'12-01-2021','15-01-2021')
        
        
        
    
    
    
    
    
    
    
    
    