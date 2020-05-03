# # - Roger Helms' capstone project to automate ACLED reporting.
# # - This file's path, working directory and remote Github repo (a/o 5/1/20):
# # -     C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\ACLED_PS2.py
# # -     C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps
# # - I upload versions of this file, as I go, to the public Github repository for Danny to check
# # -     rogerlhelms888/final_project
# # - The goal of the project is to automate the creation of bar charts and interactive maps based on a
# # -     listing of 'confict' events maintained by the aggregator ACLED.
# # - The same data comes in two different formats:
# # -     - A CSV.
# # -       Interaction.  It offers user choices to filter the data.  It requires an "I agree" from the user.
# # -       The 'Datatool' page: https://acleddata.com/data-export-tool/
# # -       Example at 5/1/20: :\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\test\2020-02-01-2020-04-29-Caucasus_and_Central_Asia.csv'
# # -     - An XLSX table.
# # -       Interaction.  No clicking or agreement is required, but the file name changes, predictably, each week.
# # -       The 'Curated' page: https://acleddata.com/curated-data-files/
# # -       URL of the download button at 5/1/20:  https://acleddata.com/download/18750/
# # -       Example at 5/1/20:
# # -       C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\CCA_2017-2020_Apr25.xlsx
# # -       https://acleddata.com/download/18750/
#
#
import datetime
import pandas as pd
import numpy as np

#
#
# # - create a dataframe from the XLSX downloaded from ACLEDs DataTool.
# # -    The current one is for 1/1/17 thru 4/25/20 as of 5/1/20 for all Central Asia & Caucuses and all event types.
# df = pd.read_excel(   # <<<<  removed slash.  OK?
# r'C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\CCA_2017-2020_Apr25.xlsx')
# # - display the newly created dataframe
# print(df.head())
#
# # - display the dataframe's columns' names as a list:
# current_ACLED_cols=[]
# for my_col in df.columns:
#      current_ACLED_cols.append(my_col)
# print('current_ACLED_cols:\n {}'.format (current_ACLED_cols))
# # -    ['ISO', 'EVENT_ID_CNTY', 'EVENT_ID_NO_CNTY', 'EVENT_DATE', 'YEAR', 'TIME_PRECISION', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'ACTOR1', 'ASSOC_ACTOR_1', 'INTER1', 'ACTOR2', 'ASSOC_ACTOR_2', 'INTER2', 'INTERACTION', 'REGION', 'COUNTRY', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION', 'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', 'SOURCE', 'SOURCE_SCALE', 'NOTES', 'FATALITIES', 'TIMESTAMP']
#
# # - Control.  Did we get the columns we expect from the newly read CSV file?
# # - (I'm not sure what to do to get the results of this test in front of human eyes.)
# original_ACLED_cols= ['ISO', 'EVENT_ID_CNTY', 'EVENT_ID_NO_CNTY', 'EVENT_DATE', 'YEAR', 'TIME_PRECISION', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'ACTOR1', 'ASSOC_ACTOR_1', 'INTER1', 'ACTOR2', 'ASSOC_ACTOR_2', 'INTER2', 'INTERACTION', 'REGION', 'COUNTRY', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION', 'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', 'SOURCE', 'SOURCE_SCALE', 'NOTES', 'FATALITIES', 'TIMESTAMP']
# if current_ACLED_cols == original_ACLED_cols:
#     print('OK. We got the columns we expected from ACLEDs curated XSLX file')
# elif current_ACLED_cols != original_ACLED_cols:
#     print('ERROR: The newly loaded columns are not the same as in older versions of the Datatool CSV')
# else:\
#     print ('ERROR: Unexpected test result.  Check code.')
#
# index = df.index
# number_of_rows = len(df.index)
# print('Row count before dropping other countries: {}.'.format(number_of_rows))
# # 64893 at 4/25/20
#
# # - Filter.  Remove any records not for Afghanistan.
# df = df[df['COUNTRY'] == 'Afghanistan']
# number_of_rows = len(df.index)
# print('row count after dropping other countries: {}.'.format(number_of_rows))
# # 4039 at 4/25/20
# #
# # - Recast event_date, which looks like this: 01 February 2020, as a chronologically sortable date, to a new column.
# df = df.assign(event_date_num=pd.to_datetime(df['EVENT_DATE']))  # ACLED only identifies time to the day.
# # # - Review and compare the the original and newly cast date columns:
# print(df[['EVENT_DATE','event_date_num']])
# #
# # - They look good at 5/1/20:
# # - 4        25 April 2020     2020-04-25
# # - ...                ...            ...
# # - 3247  01 February 2020     2020-02-01
# #
# # - Control.  Are there any records outside of the expected range of dates?  See the range of dates reported
# # - immediately above, for the current values.
# # - Earliest Date.  The earliest expected date will probably never change if we're only dealing with Afghan records.
# earliest_expected_date = pd.to_datetime('01 January 2017')  # A hardcoded date that will not change if we're only dealing with Afghan data.
# print('The earliest_expected_date: {}'.format(earliest_expected_date))
# earliest_actual_date = df['event_date_num'].min()
# print('The earliest_actual_date: {}'.format(earliest_actual_date))
# if earliest_expected_date == earliest_actual_date:
#     print('OK. The earliest actual date is equal to the earliest expected date of Feb. 1, 2020.')
# elif earliest_expected_date < earliest_actual_date:
#     print('ERROR.  The earliest actual date is later than the earliest expected date of  Feb. 1, 2020.')
# elif earliest_expected_date > earliest_actual_date:
#     print('ERROR.  The earliest actual date is earlier than the earliest expected date of  Feb. 1, 2020.')
# else:
#     print ('ERROR. Unexpected result comparing expected and actual earliest date. Check code.')
#
# # - Latest Date.  The latest expected date will change every week.
# # - You get the date from the ACLED site each week, and 'input' it here.
# latest_date_as_input = input ("  ! ENTER the year, month, and day, like : " '25 April 2020') # <<<< not yet tested
# # eg.  df = df.assign(event_date_num=pd.to_datetime(df['EVENT_DATE']))
#
# latest_expected_date = pd.to_datetime(latest_date_as_input)  # year, mo, day of most recent date covered by new ACLED table.
# print('The latest_expected_date: {}'.format(latest_expected_date))
# latest_actual_date = df['event_date_num'].max()
# print('The latest_actual_date: {}'.format(latest_actual_date))
# if latest_expected_date == latest_actual_date:
#     print('OK. The latest actual date is equal to the latest expected date of {}.'.format(latest_expected_date))
# elif latest_expected_date < latest_actual_date:
#     print('ERROR.  The latest actual date is later than the latest expected date of {}.'.format(latest_expected_date))
# elif latest_expected_date > latest_actual_date:
#     print('ERROR.  The latest actual date is earlier than the latest expected date of {}.'.format(latest_expected_date))
# else:
#     print('ERROR. Unexpected result comparing expected and actual latest date. Check code.'.format(latest_expected_date))
#
# # - Filter field: event_type
# # - Look at a unique list of event_type values
# # df_event_types=df.event_type.drop_duplicates()
# # print(df_event_types)
# # - 0                         Battles  << we want
# # - 2                        Protests
# # - 4      Explosions/Remote violence  << we want
# # - 10     Violence against civilians  << we want
# # - 12         Strategic developments
# # - 144                         Riots
#
# df = df[(df.EVENT_TYPE == 'Battles') \
#          | (df.EVENT_TYPE == 'Explosions/Remote violence') \
#           | (df.EVENT_TYPE == 'Violence against civilians')]   # works
# # - Dump useless columns to reduce size
# df=df[['EVENT_ID_CNTY','EVENT_DATE', 'event_date_num', 'TIME_PRECISION', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'ACTOR1', 'ACTOR2', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION', 'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', 'SOURCE', 'SOURCE_SCALE', 'FATALITIES']]
#
# number_of_rows = len(df.index)
# print('row count after dropping non-violent events: {}.'.format(number_of_rows))
# #
# # - Review
# print('Review.  Fields look ok?')
# print (df[['EVENT_DATE','event_date_num','EVENT_TYPE']]) # I can't get this line to work.  Not vital.
#
# # - START  DURING DEVELOPMENT ONLY  Filter down to the period 1/1/19 to date to speed processing, and
# # - create a copy to this point of processing so we don't have to wait so long to rerun our latest changes..
# df = df[df['event_date_num'] >= pd.to_datetime('1 January 2019')]
# number_of_rows = len(df.index)
# print('row count after dropping first two years: {}.'.format(number_of_rows))
# # - 16096  3,120 KB
#
# # - save the copy
# df.to_csv('df_filtered.csv')

# - Read in the filtered file
df = pd.read_csv('df_filtered.csv')
number_of_rows = len(df.index)
print('row count of reopened df_filtered.csv.  S/B the same. {}.'.format(number_of_rows))

# add an EVENT_COUNT column of 1's to permit summing to day counts or week counts.
df['EVENT_COUNT'] = 1

# - END  DURING DEVELOPMENT ONLY

df_by_day = df.groupby(['event_date_num']).sum()
print(df_by_day)

# dump useless cols from df_by_day
#  Works
df_by_day = df_by_day[['event_date_num','FATALITIES','EVENT_COUNT']]
print(df_by_day)

# - populate a new column with the dayofyear (eg. Jan 1 = 1, Jan 2 = 2... Feb 1 = 32...)
# df_by_day['DAY_OF_YEAR'] = df_by_day['event_date_num'].dt.dayofyear
# print(df_by_day)

# df['day_of_year'] = df['date_given'].dt.dayofyear  # example to delete
# print(df)




