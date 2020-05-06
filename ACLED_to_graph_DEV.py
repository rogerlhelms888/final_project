# # - Roger Helms' capstone project to automate ACLED reporting TO GRAPH.
# # -     (There is also a TO MAP script that opens by opening a CSV perpared in the current script.
# # -     C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\ACLED_to_map_DEV.py
# # - This file's path, working directory and remote Github repo (a/o 5/1/20):
# # -     C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\ACLED_to_graph_DEV.py
# # -     C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps
# # - I upload versions of this file, as I go, to the public Github repository for Danny to check
# # -     rogerlhelms888/final_project    my Github credentials are in my LastPass
# # - The goal of the project is to automate the creation of bar charts and interactive maps based on a
# # -     listing of 'confict' events maintained by the aggregator ACLED.
# # - The data comes as an XLSX table.
# # -       Source: 'Curated' page: https://acleddata.com/curated-data-files/
# # -       URL of the download button at 5/1/20:  https://acleddata.com/download/18750/
# # -       Interaction.  No clicking or agreement is required, but the file name changes, predictably, each week.
# # -       Example at 5/1/20:
# # -       C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\CCA_2017-2020_Apr25.xlsx
# # -       https://acleddata.com/download/18750/
#
#
import datetime
import pandas as pd
import numpy as np

# # configure PyCharm to see more columns across more of the screen
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# # - USER ACTION: Create a dataframe from the XLSX downloaded from ACLED's Curated files by downloading the most recent
# # - EXCEL file from it and placing it in the folder:
# # -    C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps
# # -    The current one is for 1/1/17 thru 4/25/20 as of 5/1/20 for all Central Asia & Caucuses and all event types.
df = pd.read_excel(
   r'C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\CCA_2017-2020_May02.xlsx')

# # - display the newly created dataframe
# print(df.head())

# # - display the dataframe's columns' names as a list:
current_ACLED_cols=[]
for my_col in df.columns:
    current_ACLED_cols.append(my_col)
print('current_ACLED_cols:\n {}'.format(current_ACLED_cols))
# # PRESERVE for reference:
# #    Expected column names as of 5/6/20:
# # -  ['ISO', 'EVENT_ID_CNTY', 'EVENT_ID_NO_CNTY', 'EVENT_DATE', 'YEAR', 'TIME_PRECISION', 'EVENT_TYPE',
# # -   'SUB_EVENT_TYPE', 'ACTOR1', 'ASSOC_ACTOR_1', 'INTER1', 'ACTOR2', 'ASSOC_ACTOR_2', 'INTER2', 'INTERACTION',
# # -   'REGION', 'COUNTRY', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION', 'LATITUDE', 'LONGITUDE', 'GEO_PRECISION',
# # -   'SOURCE', 'SOURCE_SCALE', 'NOTES', 'FATALITIES', 'TIMESTAMP']

# # - CONTROL.  Did we get the columns we expect from the newly read CSV file?
# # -    Compare the expected column names to the 'read' ones of the latest ACLED curated file.
original_ACLED_cols = ['ISO', 'EVENT_ID_CNTY', 'EVENT_ID_NO_CNTY', 'EVENT_DATE', 'YEAR', 'TIME_PRECISION', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'ACTOR1', 'ASSOC_ACTOR_1', 'INTER1', 'ACTOR2', 'ASSOC_ACTOR_2', 'INTER2', 'INTERACTION', 'REGION', 'COUNTRY', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION', 'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', 'SOURCE', 'SOURCE_SCALE', 'NOTES', 'FATALITIES', 'TIMESTAMP']
if current_ACLED_cols == original_ACLED_cols:
    print('OK. We got the columns we expected from ACLEDs curated XSLX file')
elif current_ACLED_cols != original_ACLED_cols:
    print('ERROR: The newly loaded columns are not the same as in older versions of the Datatool CSV')
else:
    print('ERROR: Unexpected test result.  Check code.')

index = df.index
number_of_rows = len(df.index)
print('Row count before dropping other countries: {}.'.format(number_of_rows))
# # 64893 at 4/25/20

# # - Filter.  Remove any records not for Afghanistan.
df = df[df['COUNTRY'] == 'Afghanistan']
number_of_rows = len(df.index)
print('row count after dropping other countries: {}.'.format(number_of_rows))
# # - 4039 at 4/25/20

# # - Recast event_date, which looks like this: 01 February 2020, as a chronologically sortable date, to a new column.
df = df.assign(EVENT_DATE_NUM=pd.to_datetime(df['EVENT_DATE']))
# # - Review and compare the the original and newly cast date columns:
print(df[['EVENT_DATE', 'EVENT_DATE_NUM']])

# # - They look good at 5/1/20:
# # - 4        25 April 2020     2020-04-25
# # - ...                ...            ...
# # - 3247  01 February 2020     2020-02-01

# # - Control.  Are there any records outside of the expected range of dates?  See the range of dates reported
# # - immediately above, for the current values.
# # - Earliest Date.  The earliest expected date will probably never change if we're only dealing with Afghan records.
# # - It is a hardcoded date that will not change, as long as we're only dealing with Afghan data.
earliest_expected_date = pd.to_datetime('01 January 2017')
print('The earliest_expected_date: {}'.format(earliest_expected_date))
earliest_actual_date = df['EVENT_DATE_NUM'].min()
print('The earliest_actual_date: {}'.format(earliest_actual_date))
if earliest_expected_date == earliest_actual_date:
    print('OK. The earliest actual date is equal to the earliest expected date of Feb. 1, 2020.')
elif earliest_expected_date < earliest_actual_date:
    print('ERROR.  The earliest actual date is later than the earliest expected date of  Feb. 1, 2020.')
elif earliest_expected_date > earliest_actual_date:
    print('ERROR.  The earliest actual date is earlier than the earliest expected date of  Feb. 1, 2020.')
else:
    print('ERROR. Unexpected result comparing expected and actual earliest date. Check code.')

# # - Latest Date.  The latest expected date will change every week.
# # - You get the date from the ACLED site each week, and 'input' it here.
# # - Temporarily disabled during DEV. <<<
# latest_date_as_input = input ("  ! ENTER the year, month, and day, like : " '25 April 2020')
latest_date_as_input = '25 April 2020'  # Comment out this row when the one above is uncommented in prod.

# # convert the inputted date to datetime (year, mo, day) so we can compare it to what we got.
latest_expected_date = pd.to_datetime(latest_date_as_input)
print('The latest_expected_date: {}'.format(latest_expected_date))
latest_actual_date = df['EVENT_DATE_NUM'].max()
print('The latest_actual_date: {}'.format(latest_actual_date))
if latest_expected_date == latest_actual_date:
    print('OK. The latest actual date is equal to the latest expected date of {}.'.format(latest_expected_date))
elif latest_expected_date < latest_actual_date:
    print('ERROR.  The latest actual date is later than the latest expected date of {}.'.format(latest_expected_date))
elif latest_expected_date > latest_actual_date:
    print('ERROR.  The latest actual date is earlier than the latest expected date of {}.'.format(latest_expected_date))
else:
    print('ERROR. Unexpected result comparing expected vs actual latest date. Check code.'.format(latest_expected_date))

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

df = df[(df.EVENT_TYPE == 'Battles') 
        | (df.EVENT_TYPE == 'Explosions/Remote violence')
        | (df.EVENT_TYPE == 'Violence against civilians')]   # works
# # - Dump useless columns to reduce size
df = df[['EVENT_ID_CNTY', 'EVENT_DATE', 'EVENT_DATE_NUM', 'TIME_PRECISION', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'ACTOR1', 'ACTOR2', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION', 'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', 'SOURCE', 'SOURCE_SCALE', 'FATALITIES']]

number_of_rows = len(df.index)
print('row count after dropping non-violent events: {}.'.format(number_of_rows))

# # - Review
# print('Review.  Fields look ok?')
print(df[['EVENT_DATE', 'EVENT_DATE_NUM', 'EVENT_TYPE']])  # I can't get this line to work.  Not vital.

# # - START  DURING DEVELOPMENT ONLY
# # - Filter down to the period 1/1/19 to date to speed processing, and
# # - Create a copy to this point of processing so we don't have to wait so long to rerun our latest changes.
df = df[df['EVENT_DATE_NUM'] >= pd.to_datetime('1 January 2019')]
number_of_rows = len(df.index)
print('row count after dropping first two years: {}.'.format(number_of_rows))
# # - 16096  3,120 KB

# # - save the copy
df.to_csv('df_filtered.csv')

# - Read in the filtered file
df = pd.read_csv('df_filtered.csv')
number_of_rows = len(df.index)
print('row count of reopened df_filtered.csv.  S/B the same. {}.'.format(number_of_rows))

# - add an EVENT_COUNT column of 1's to permit summing to day counts or week counts.
df['EVENT_COUNT'] = 1

# - END  DURING DEVELOPMENT ONLY

# Group by date and sum numeric columns.  Works.
df_by_day = df.groupby(['EVENT_DATE_NUM']).sum()
print(df_by_day)
number_of_rows = len(df_by_day.index)
print('row count of grouped df: {}.'.format(number_of_rows))

#                        FATALITIES  EVENT_COUNT
# EVENT_DATE_NUM
# 2019-01-01             154           33
# 2019-01-02              80           28

# - dump useless cols (like lats and longs) from df_by_day.  Works.
df_by_day = df_by_day[['FATALITIES', 'EVENT_COUNT']]
print(df_by_day)

# - Get the EVENT_DATE_NUM index back as a column.
df_by_day.reset_index(inplace=True)
print(df_by_day)

#         EVENT_DATE_NUM     FATALITIES    EVENT_COUNT
# 0       2019-01-01         154           33
# 1       2019-01-02          80           28

# - Populate a new column with the dayofyear (eg. Jan 1 = 1, Jan 2 = 2... Feb 1 = 32...)
# - But first create a new column that Pandas will understand as being datetimelike.  This is needed because
# - I get the error messsage "AttributeError: Can only use .dt accessor with datetimelike values"
# - when I try to assign day of year based on the 'EVENT_DATE_NUM' field retrieved from the index.
# - Works!
df_by_day = df_by_day.assign(EVENT_DATE_NUM_NUM=pd.to_datetime(df_by_day['EVENT_DATE_NUM']))
# - Populate a new column with the dayofyear
df_by_day['DAY_OF_YEAR'] = df_by_day['EVENT_DATE_NUM_NUM'].dt.dayofyear
print('checkpoint - delete for PROD')
print(df_by_day[['FATALITIES', 'EVENT_COUNT', 'EVENT_DATE_NUM_NUM', 'DAY_OF_YEAR']])

# # - Now establish columns for FATALITIES and for EVENT_COUNT for each year, like this:

# # - DAY_OF_YEAR     FATALITIES_2020  EVENT_COUNTS_2020   FATALITIES_2019  EVENT_COUNTS_2019...
# # - 1               123                44                154                 33
# # - 2               123                40                135                 30


# # - Do this by creating a series of integers 1-366 days and merging it to
# # -    extracts of the df_by_day dataframe for 2020 and, separately, for 2019.
# # -    The join would be on the DAY_OF_YEAR values.

# Copy out the 2020 records, rename their columns
df_2020 = df_by_day[df_by_day['EVENT_DATE_NUM_NUM'] >= pd.to_datetime('1 January 2020')]
df_2020 = df_2020[df_2020['EVENT_DATE_NUM_NUM'] < pd.to_datetime('1 January 2021')]
df_2020.rename(columns={'FATALITIES': 'FATALITIES_2020'}, inplace=True)
df_2020.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2020'}, inplace=True)
# df_2020.set_index('DAY_OF_YEAR', inplace=True) # not needed for merge
print('Here is 2020:')
print(df_2020[['EVENT_DATE_NUM', 'FATALITIES_2020', 'EVENT_COUNT_2020', 'DAY_OF_YEAR']])

df_2019 = df_by_day[df_by_day['EVENT_DATE_NUM_NUM'] >= pd.to_datetime('1 January 2019')]
df_2019 = df_2019[df_2019['EVENT_DATE_NUM_NUM'] < pd.to_datetime('1 January 2020')]
df_2019.rename(columns={'FATALITIES': 'FATALITIES_2019'}, inplace=True)
df_2019.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2019'}, inplace=True)
# df_2019.set_index('DAY_OF_YEAR', inplace=True) # not needed for merge
print('Here is 2019:')
print(df_2019[['EVENT_DATE_NUM', 'FATALITIES_2019', 'EVENT_COUNT_2019', 'DAY_OF_YEAR']])

# # - We don't use 2018 or 2017 so far, for want of interest.  We have the data and could.

# # - Create a one column dataframe of integers 1-366 to use in merges.  We need this
# # - because we won't necessarily have events for every day (two days were missing in 2019).
# # - We will need every day, populated or not, for the bar charts.
df_all_days = pd.DataFrame({'DAY_OF_YEAR': [range(1, 366, 1)]}, index=[range(1, 366, 1)])
print('Here is the type of df_all_days: {}'.format(type(df_all_days)))
print('Here is a print of df_all_days: {}'.format(df_all_days))

# # - Merge the list of 366 and the 2019 lists.  We need to do this to make sure we have 366 rows in the
# # - output, even though a couple of days are missing in 2019.  (But I can't get this first merge
# # - to work, so I'm leaving it commented for now, and will fix later)
# #     df_2019 = pd.merge(df_all_days, df_2019, on='DAY_OF_YEAR', how='outer') # didn't work <<< !!! Fix later

# # - Merge 2019 and 2020 into a single table using an outer join.
# # - There may have been one day in 2020 without any events.  None in 2019.
df_merged = pd.merge(df_2020, df_2019, on='DAY_OF_YEAR', how='outer')
print(df_merged[['EVENT_DATE_NUM_y', 'EVENT_COUNT_2019', 'FATALITIES_2019', 'EVENT_COUNT_2020', 'FATALITIES_2020']])
# # - There are only 364 rows (last index was 363).  I am be missing two days that were in neither list.  That
# # -    problem would be fixed if I could address the problem merging the df_all_days with the df_2019, above.

# # - Write the file to disk.
# # -    Here is the path: C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\to_AGOL.CSV
df_merged.to_csv('to_AGOL_latest.CSV')

