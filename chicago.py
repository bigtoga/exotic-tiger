#importing dependencies and setting app token
import pandas as pd
from datetime import date, datetime
import numpy as np
from sodapy import Socrata
import csv
import sqlite3
# from api_keys import MyAppToken

# Heroku support
# Create the .env file:
# heroku config:get MyToken -s --app exotic-tiger >> .env
import os
from dotenv import load_dotenv

# # Retrieves config var from Heroku. Place in .env file if running locally
MyAppToken = os.getenv("MyToken")

crime_data = "ijzp-q8t2"
client = Socrata("data.cityofchicago.org", MyAppToken)
max_rows_to_return = 10

# checking the day of the month and printing the result, this is used to filter the dataframe later
today = date.today()
daynum = today.strftime("%d")
month = today.strftime("%m")
day = int(daynum) - 8
# print(f'      --- chicago.py: Most recent day/month: {month}-{day}')


def getData():
    print('      --- chicago.py getData(): entering getData()')

    def getRawData(year):
        print(f'             --- chicago.py getRawData({year}): entering getRawData()')

        where_clause = f"Date BETWEEN '{year}-01-01' AND '{year}-{month}-{day}'"
        # where_clause = where_clause + " AND  'Primary Type' IN ('THEFT', 'BATTERY')"
        # where_clause = "'Primary Type' IN ('THEFT', 'BATTERY')"
        
        print(f'                --- WHERE clause: {where_clause}')
        
        print(f'                --- calling API now w limit of {max_rows_to_return} rows requested with token {MyAppToken}')
        df = pd.DataFrame(
            client.get(
                crime_data, 
                where=where_clause,
                limit=max_rows_to_return,
                exclude_system_fields=True
            )
        )
        client.close()

        print('                --- API call complete - on to feature engineering...')
        # reformatting the data from the api call and organizing the results
        df['day'] = pd.DatetimeIndex(df['date']).day
        df['month'] = pd.DatetimeIndex(df['date']).month
        df['year'] = pd.DatetimeIndex(df['date']).year
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['month_day'] = pd.to_datetime(df['date']).dt.strftime('%m-%d')
        df["primary_type"] = df["primary_type"].str.lower().str.title()

        print('                --- returning dataframe "dfReturn" w 7 columns')
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
        
        print('')
        return dfReturn

    print('         --- chicago.py getData(): About to call sodapy + API...')
    df2020 = getRawData('2020')
    df2019 = getRawData('2019')
    df2018 = getRawData('2018')
    print('')

    # printing shape of all results to confirm the data is correct  
    print('         --- chicago.py getData(): Finished! Results: ')
    print(f'         --- chicago.py getData():    - 2020 data (df2020): {len(df2020.index)} rows')
    print(f'         --- chicago.py getData():    - 2019 data (df2019): {len(df2019.index)} rows')
    print(f'         --- chicago.py getData():    - 2018 data (df2018): {len(df2018.index)} rows')
    print('')

    # combining the 2018, 2019, and 2020 dataframes into one
    print('         --- chicago.py getData(): Combining the 3 dataframes into 1 using pd.concat()')
    dataframes = [df2018, df2019, df2020]
    final_df = pd.concat(dataframes)
    print(f'         --- chicago.py getData(): final_df contains {len(final_df.index)} rows')
    print('')

    #########################################################
    #Creating AGG's and Group By's, 5 in total
    #########################################################

    print('         --- chicago.py getData(): Group by: date + month_day')
    aggs_overall = final_df.groupby(["date", "month_day"]).agg({'day': [np.count_nonzero]}).reset_index() 
    aggs_overall.columns = ["date", "month_day", "crimes_committed"]
    aggs_overall.to_csv("static/data/crime_by_date.csv")

    dfCSV = aggs_overall.set_index('date')

    print('         --- chicago.py getData(): Group by: date + month_day + primary_type')
    aggs_by_date_type = final_df.groupby(["date", "month_day", "primary_type"]).agg({'day': [np.count_nonzero]}).reset_index() 
    aggs_by_date_type.columns = ["date", "month_day", "primary_type", "crimes_committed"]
    aggs_by_date_type = aggs_by_date_type.set_index(pd.DatetimeIndex(aggs_by_date_type['date']))
    aggs_by_date_type = aggs_by_date_type.drop(['date'], axis=1)
    aggs_by_date_type.to_csv('static/data/final_Chicago_data_total_crime_by_date_and_type.csv')

    print('         --- chicago.py getData(): Group by: month_day + year + domestic')
    grouped_month_day = final_df.groupby(['month_day', 'year','domestic']).count()
    grouped_month_day = grouped_month_day.drop(columns = ['date','day','month'])
    grouped_month_day = grouped_month_day.rename(columns={"primary_type": "month_total_crimes"})
    grouped_month_day.reset_index(inplace=True)
    grouped_month_day.to_csv('static/data/grouped_month_day.csv', index=False)

    ############################################################
    #creating database from all dataframes created in chicago.py
    ############################################################

    print('')
    print('=' * 100)
    print('         --- chicago.py getData(): Connect to sqlite database "chicago_data.sqlite"')
    print('=' * 100)

    #creates sql lite file called chicago_data and adds a cursor so we can create queries
    db = sqlite3.connect('chicago_data.sqlite')
    #inserts only new values from api call into sqlite file

    final_df.to_sql('chicago_data', db, if_exists = 'replace')
    print(f'            --- created table "chicago_data" with {len(final_df.index)} rows')

    aggs_overall.to_sql('aggs_overall', db, if_exists = 'replace')
    print(f'            --- created table "aggs_overall" with {len(aggs_overall.index)} rows')

    aggs_by_date_type.to_sql('aggs_by_date_type', db, if_exists = 'replace')
    print(f'            --- created table "aggs_by_date_type" with {len(aggs_by_date_type.index)} rows')

    dfCSV.to_sql('dfCSV', db, if_exists = 'replace')
    print(f'            --- created table "dfCSV" with {len(dfCSV.index)} rows')

    grouped_month_day.to_sql('groupby_df', db, if_exists = 'replace')
    print(f'            --- created table "groupby_df" with {len(grouped_month_day)} rows') # has no index

    db.close()

    print('')
    print('      --- chicago.py getData(): done!')    
    print('')

if __name__ == '__main__':
    getData()


