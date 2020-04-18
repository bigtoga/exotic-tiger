#importing dependencies and setting app token
import pandas as pd
from datetime import date, datetime
import numpy as np
from sodapy import Socrata
import csv
import sqlite3
from api_keys import MyAppToken

crime_data = "ijzp-q8t2"
client = Socrata("data.cityofchicago.org", MyAppToken)

#checking the day of the month and printing the result, this is used to filter the dataframe later
today = date.today()
daynum = today.strftime("%d")
month = today.strftime("%m")
day = int(daynum) - 8
print(f"Day: {day} \nMonth: {month}")

def getData():
    

    def getRawData(year):
        where_clause = f"Date BETWEEN '{year}-01-01' AND '{year}-{month}-{day}'";
        #where_clause = where_clause + " AND  'Primary Type' IN ('THEFT', 'BATTERY')"
        #where_clause = "'Primary Type' IN ('THEFT', 'BATTERY')"
        
        df = pd.DataFrame(
            client.get(
                crime_data, 
                where=where_clause,
                limit=100000,
                exclude_system_fields=True
            )
        )
        client.close()

        #reformatting the data from the api call and organizing the results
        df['day'] = pd.DatetimeIndex(df['date']).day
        df['month'] = pd.DatetimeIndex(df['date']).month
        df['year'] = pd.DatetimeIndex(df['date']).year
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['month_day'] = pd.to_datetime(df['date']).dt.strftime('%m-%d')
        df["primary_type"] = df["primary_type"].str.lower().str.title()

        # Organize column order: 
        dfReturn = df[[
            "primary_type"
            , "date"
            , "month_day"
            , "day"
            , "month"
            , "year"
            , "domestic"
        ]]
        
        return dfReturn

    df2020 = getRawData('2020')
    df2019 = getRawData('2019')
    df2018 = getRawData('2018')

    #printing shape of all results to confirm the data is correct  
    print(f"2020: {df2020.shape} 2019: {df2019.shape} 2018: {df2018.shape}")

    #combining the 2018, 2019, and 2020 dataframes into one
    dataframes = [df2018, df2019, df2020]
    final_df = pd.concat(dataframes)
    print(f"Final DF Rows/Columns: {final_df.shape}")

    #########################################################
    #Creating AGG's and Group By's, 5 in total
    #########################################################

    aggs_overall = final_df.groupby(["date", "month_day"]).agg({'day': [np.count_nonzero]}).reset_index() 
    aggs_overall.columns = ["date", "month_day", "crimes_committed"]
    aggs_overall.to_csv("static/data/crime_by_date.csv")

    dfCSV = aggs_overall.set_index('date')

    aggs_by_date_type = final_df.groupby(["date", "month_day", "primary_type"]).agg({'day': [np.count_nonzero]}).reset_index() 
    aggs_by_date_type.columns = ["date", "month_day", "primary_type", "crimes_committed"]
    aggs_by_date_type = aggs_by_date_type.set_index(pd.DatetimeIndex(aggs_by_date_type['date']))
    aggs_by_date_type = aggs_by_date_type.drop(['date'], axis=1)
    aggs_by_date_type.to_csv('static/data/final_Chicago_data_total_crime_by_date_and_type.csv')

    grouped_month_day = final_df.groupby(['month_day', 'year','domestic']).count()
    grouped_month_day = grouped_month_day.drop(columns = ['date','day','month'])
    grouped_month_day = grouped_month_day.rename(columns={"primary_type": "month_total_crimes"})
    grouped_month_day.reset_index(inplace=True)
    grouped_month_day.to_csv('static/data/grouped_month_day.csv', index=False)

    ############################################################
    #creating database from all dataframes created in chicago.py
    ############################################################

    #creates sql lite file called chicago_data and adds a cursor so we can create queries
    db = sqlite3.connect('chicago_data.sqlite')
    #inserts only new values from api call into sqlite file
    final_df.to_sql('chicago_data', db, if_exists = 'replace')
    aggs_overall.to_sql('aggs_overall', db, if_exists = 'replace')
    aggs_by_date_type.to_sql('aggs_by_date_type', db, if_exists = 'replace')
    dfCSV.to_sql('dfCSV', db, if_exists = 'replace')
    grouped_month_day.to_sql('groupby_df', db, if_exists = 'replace')
    db.close()

if __name__ == '__main__':
    getData()


