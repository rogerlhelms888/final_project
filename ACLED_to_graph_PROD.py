# # - This is latest version, on GitHub.  It superceds a file of the same name in a different directory.

# # - REMEMBER that there is an INPUT response, the last date expected from ACLED, when you run this script!

# # - Roger Helms' capstone project to automate ACLED reporting TO GRAPH.
# # - This script file's path:
# # -     C:\Users\Roger Helms\Documents\GitHub\final_project\ACLED_to_map_DEV.py
# # - Stored in this remote GitHub repo: https://github.com/rogerlhelms888/final_project
# # -     My Github credentials are in my LastPass
# # - Stored in this local Github repo:  C:\Users\Roger Helms\Documents\GitHub\final_project
# # - The local github path:  C:\Users\Roger Helms\Documents\GitHub\final_project\ACLED_to_graph_DEV.py
# # - The goal of the project is to automate the creation of bar charts and interactive maps based on a
# # -     listing of 'confict' events maintained by the aggregator ACLED.
# # - The data comes as an XLSX table.
# # -       Source: 'Curated' page: https://acleddata.com/curated-data-files/
# # -       URL of the download button at 5/1/20:  https://acleddata.com/download/18750/
# # -       Interaction.  No clicking or agreement is required, but the file name changes, predictably, each week.
# # -       Example at 5/1/20:
# # -       C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\CCA_2017-2020_Apr25.xlsx
# # -       https://acleddata.com/download/18750/
# # - Output.  This script creates two CSV's:
# # -       - a CSV of event counts and fatalities by day:           to_AGOL_latest.CSV
# # -       - a CSV of event counts and fatalities by coordinate:    df_filtered.csv
#
import datetime as dt
import pandas as pd
import numpy as np
from IPython.display import IFrame
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sns
import math as math

# # configure PyCharm to see more columns across more of the screen than the default permits.
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
    print('OK. The earliest actual date is equal to the earliest expected date of Jan. 1, 2020.')
elif earliest_expected_date < earliest_actual_date:
    print('ERROR.  The earliest actual date is later than the earliest expected date of  Jan. 1, 2020.')
elif earliest_expected_date > earliest_actual_date:
    print('ERROR.  The earliest actual date is earlier than the earliest expected date of  Jan. 1, 2020.')
else:
    print('ERROR. Unexpected result comparing expected and actual earliest date. Check code.')

# # - Latest Date.  The latest expected date will change every week.
# # - You get the date from the ACLED site each week, and 'input' it here.
# # - Next row normally commented during DEV, and uncommented during production.
latest_date_as_input = input ("  ! ENTER the year, month, and day, like : " '25 April 2020')
# # - latest_date_as_input = '25 April 2020'  # Used during DEV.  Comment out this row and use the one above in PROD.

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

if latest_actual_date != latest_expected_date:
    raise Exception('EXCEPTION.  The last ACTUAL date was not the same as the last EXPECTED date: {}'.format(x))

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
# # - Dump useless columns to reduce size, keeping only the ones listed below:
df = df[['EVENT_ID_CNTY', 'EVENT_DATE', 'EVENT_DATE_NUM', 'TIME_PRECISION', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'ACTOR1', \
         'ACTOR2', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION', 'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', 'SOURCE',\
         'SOURCE_SCALE', 'FATALITIES']]

# # REVIEW
number_of_rows = len(df.index)
print('row count after dropping non-violent events: {}.'.format(number_of_rows))

# # - Filter down to the period 1/1/19 to date.
df = df[df['EVENT_DATE_NUM'] >= pd.to_datetime('1 January 2019')]
number_of_rows = len(df.index)
# print('row count after dropping first two years: {}.'.format(number_of_rows))
# # - 16096  3,120 KB on 25 April 2020 version.

print(df['EVENT_DATE_NUM'].tail(3)) # We now expect to see the last day of ACLED's most recent update.
# # - Eliminate the records for the last day.
df = df[df['EVENT_DATE_NUM'] != pd.to_datetime(latest_date_as_input)]
# print(df['EVENT_DATE_NUM'].tail(3))  # We now don't expect to see that anemic last day of ACLED's data.

# # - Save a copy of the dataframe as filtered for later use in separate script to prepare a file to be mapped.
# # - That separate script is:
# # -    C:\Users\Roger Helms\Documents\GitHub\final_project\ACLED_to_map_DEV.py
# df.to_csv('df_filtered.csv') # <<<
df.to_csv(r'C:\Users\Roger Helms\Documents\GitHub\final_project\df_filtered.csv')
# # -------------------------------------------------------
# # Group for reporting by day or week.

# - add an EVENT_COUNT column of 1's to permit summing.
df['EVENT_COUNT'] = 1

# create a column for day of year and populate it. #<<<
# - Populate a new column with the dayofyear (eg. Jan 1 = 1, Jan 2 = 2... Feb 1 = 32...)
# - But first create a new column that Pandas will understand as being datetimelike.  This is needed because,
# -   when I try to create and populate the DAY_OF_YEAR column, I
# -    get the messsage "AttributeError: Can only use .dt accessor with datetimelike values"
# -   when I try to assign day of year based on the 'EVENT_DATE_NUM' field retrieved from the index.
df = df.assign(EVENT_DATE_NUM_NUM=pd.to_datetime(df['EVENT_DATE_NUM']))
df['DAY_OF_YEAR'] = df['EVENT_DATE_NUM_NUM'].dt.dayofyear

# Group by day and sum numeric columns.  Works.
df_by_day = df.groupby(['EVENT_DATE_NUM']).sum()
print(df_by_day)
number_of_rows = len(df_by_day.index)
print('row count of grouped df: {}.'.format(number_of_rows))


# - dump useless cols (like lats and longs) from df_by_day.  Works.
df_by_day = df_by_day[['FATALITIES', 'EVENT_COUNT']]
print(df_by_day)

# - Get the EVENT_DATE_NUM index back as a column.
df_by_day.reset_index(inplace=True)

#         EVENT_DATE_NUM     FATALITIES    EVENT_COUNT
# 0       2019-01-01         154           33
# 1       2019-01-02          80           28

# - Populate a new column with the dayofyear (eg. Jan 1 = 1, Jan 2 = 2... Feb 1 = 32...)
# - But first create a new column that Pandas will understand as being datetimelike.  This is needed because,
# -   when I try to create and populate the DAY_OF_YEAR column, I
# -    get the messsage "AttributeError: Can only use .dt accessor with datetimelike values"
# -   when I try to assign day of year based on the 'EVENT_DATE_NUM' field retrieved from the index.
# df_by_day = df_by_day.assign(EVENT_DATE_NUM_NUM=pd.to_datetime(df_by_day['EVENT_DATE_NUM'])) # <<<<<
# - Populate a new column with the dayofyear
# df_by_day['DAY_OF_YEAR'] = df_by_day['EVENT_DATE_NUM_NUM'].dt.dayofyear
# print(df_by_day[['FATALITIES', 'EVENT_COUNT', 'EVENT_DATE_NUM_NUM', 'DAY_OF_YEAR']])

# # - Now establish columns for FATALITIES and for EVENT_COUNT for each year, like this:

# # - DAY_OF_YEAR     FATALITIES_2020  EVENT_COUNTS_2020   FATALITIES_2019  EVENT_COUNTS_2019...
# # - 1               123                44                154                 33
# # - 2               123                40                135                 30


# # - Do this by creating a series of integers 1-366 days and merging it to
# # -    extracts of the df_by_day dataframe for 2020 and, separately, for 2019.
# # -    The join would be on the DAY_OF_YEAR values.

# Copy out the 2019 records into their own dataframe, then rename their columns
df_2019 = df[df['EVENT_DATE_NUM_NUM'] >= pd.to_datetime('1 January 2019')]
df_2019 = df_2019[df_2019['EVENT_DATE_NUM_NUM'] < pd.to_datetime('1 January 2020')]
df_2019.rename(columns={'FATALITIES': 'FATALITIES_2019'}, inplace=True)
df_2019.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2019'}, inplace=True)
print('Here is 2019:')
print(df_2019[['EVENT_DATE_NUM', 'FATALITIES_2019', 'EVENT_COUNT_2019', 'DAY_OF_YEAR']])
print("Print type (df_2019['DAY_OF_YEAR']:")
print(type(df_2019['DAY_OF_YEAR']))

# Copy out the 2020 records into their own dataframe, then rename their columns
df_2020 = df[df['EVENT_DATE_NUM_NUM'] >= pd.to_datetime('1 January 2020')]
df_2020 = df_2020[df_2020['EVENT_DATE_NUM_NUM'] < pd.to_datetime('1 January 2021')]
df_2020.rename(columns={'FATALITIES': 'FATALITIES_2020'}, inplace=True)
df_2020.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2020'}, inplace=True)
print('Here is 2020:')
print(df_2020[['EVENT_DATE_NUM', 'FATALITIES_2020', 'EVENT_COUNT_2020', 'DAY_OF_YEAR']])

# # - We don't use 2018 or 2017 so far, for want of interest.  We have the data and could.

# # - Create a two column dataframe of integers 1-366 to use in merges.  We need this
# # - because we won't necessarily have events for every day (two days were missing in 2019).
# # - We will need every day, populated or not, for the bar charts.
# df_all_days = pd.DataFrame({'DAY_OF_YEAR': [range(1, 366, 1)]}, index=[range(1, 366, 1)]) # <<< strange result
# #  Create a dataframe of integers 1-366 to use in merges.my_num_list = []
# num_list = range(1, 367, 1)
# for num in num_list:
#     my_num_list.append(str(num))
#
# print(my_num_list)

all_days=[]
num_list = range(1, 367, 1)
for num in num_list:
    all_days.append(num)

print(all_days)

df_all_days = pd.DataFrame({
    'DAY_OF_YEAR': (all_days)
})

# df_all_days = pd.DataFrame({
#     'DAY_OF_YEAR': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366]
# })

# # - Review
# print('print both columns of the df_all_days dataframe')
# print('Here is a print of df_all_days:')
# print(df_all_days)
# # - looks right, with 366 rows, as expected.
# print('Here is the type of df_all_days: {}'.format(type(df_all_days)))
# # - A DataFrame, as expected.


# # - Merge the list of 366 and the 2019 lists.  We need to do this to make sure we have 366 rows in the
# # - output, even though a couple of days are missing in 2019.  (But I can't get this first merge
# # - to work, so I'm leaving it commented for now, and will fix later)
df_2019 = pd.merge(df_all_days, df_2019, on='DAY_OF_YEAR', how='outer')
print('a print of df_2019, hopefully with one row per day:')
print(df_2019)

# # - Merge 2019 and 2020 into a single table using an outer join.
# # - There may have been one day in 2020 without any events.  None in 2019.
df_merged = pd.merge(df_2020, df_2019, on='DAY_OF_YEAR', how='outer')
# # print(df_merged[['EVENT_DATE_NUM', 'EVENT_COUNT_2019', 'FATALITIES_2019', 'EVENT_COUNT_2020', 'FATALITIES_2020']])
print("Here is df_merged, which gets saved here: 'to_AGOL_latest.CSV'' ")
print(df_merged)
# # - There are 366 rows (last index was 365), so we're good.

# # - Write the by_day file to disk.
df_merged.to_csv(r'C:\Users\Roger Helms\Documents\GitHub\final_project\by_day_to_Matplotlib.CSV')
# # ---------------------------------------------------------------

# # - Create a CSV by week to graph.
# # - We want full 7 day weeks, but the most recent week would always be short a day and include the
# # -    most recent day reported, which is always underpopulated.  To compensate, we will
# # -    assign ordinal weeks of the year starting with Jan 3 as the first day of week 1.
# # -    We cannot do that by bumping the EVENT_DATE_NUM_NUM values by 2 because "adddition/subtraction of
# # -    integers and integer-arrays with DatetimeArray is no longer supported."
# # -    Instead, I'll add 2 to the day of year values, then divide those values by 7 and round up to the
# # -    nearest integer to get the week of year.

# df_by_day['DAY_OF_YEAR'] = df_by_day['DAY_OF_YEAR']+3
df['DAY_OF_YEAR'] = df['DAY_OF_YEAR']+3

print('Here is the type of DAY_OF_YEAR')
print(type(df['DAY_OF_YEAR']))
# # - Add and populate a column of week_of_year
df['WEEK_OF_YEAR'] = np.floor(df['DAY_OF_YEAR']/7)
# # - REVIEW.  Looks good.
# print('print of df:')
# print(df.head(12))
# print(df.tail(8))

# Create a separate data frame of 2020, and another for 2019
# Unlike for the rollup by day, which was done on the overall file, the rollup by week must
# be done for each year separately, on the WEEK_OF_YEAR field.

print(df.EVENT_DATE_NUM) # <<<

# Copy out the 2019 records into their own dataframe, then rename their columns
df_2019_by_week = df[df['EVENT_DATE_NUM_NUM'] >= pd.to_datetime('1 January 2019')] # <<<< EVENT_DATE_NUM to EVENT_DATE_NUM_NUM
df_2019_by_week = df[df['EVENT_DATE_NUM_NUM'] < pd.to_datetime('1 January 2020')]  # <<<< EVENT_DATE_NUM to EVENT_DATE_NUM_NUM
df_2019_by_week.rename(columns={'FATALITIES': 'FATALITIES_2019_WEEKLY'}, inplace=True)
df_2019_by_week.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2019_WEEKLY'}, inplace=True)
print('The FATALITIES_2019_WEEKLY and EVENT_COUNT_2019_WEEKLY columns are just placeholders so far:')
# print(df_2019_by_week[['EVENT_DATE_NUM', 'FATALITIES_2019_WEEKLY', 'EVENT_COUNT_2019_WEEKLY', 'DAY_OF_YEAR', 'WEEK_OF_YEAR']])

# Copy out the 2019 records into their own dataframe, then rename their columns
df_2020_by_week = df[df['EVENT_DATE_NUM_NUM'] >= pd.to_datetime('1 January 2020')] # <<<< EVENT_DATE_NUM to EVENT_DATE_NUM_NUM
df_2020_by_week = df[df['EVENT_DATE_NUM_NUM'] < pd.to_datetime('1 January 2021')]  # <<<< EVENT_DATE_NUM to EVENT_DATE_NUM_NUM
df_2020_by_week.rename(columns={'FATALITIES': 'FATALITIES_2020_WEEKLY'}, inplace=True)
df_2020_by_week.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2020_WEEKLY'}, inplace=True)
print('The FATALITIES_2020_WEEKLY and EVENT_COUNT_2020_WEEKLY columns are just placeholders so far:')
# print(df_2020_by_week[['EVENT_DATE_NUM', 'FATALITIES_2020_WEEKLY', 'EVENT_COUNT_2020_WEEKLY', 'DAY_OF_YEAR', 'WEEK_OF_YEAR']])

# # Group by week of year, and sum numeric columns.
# # - 2019 group
df_2019_by_week = df_2020_by_week.groupby(['WEEK_OF_YEAR']).sum()
print(df_2019_by_week)
number_of_rows = len(df_2019_by_week .index)
print('-- Row count of grouped df_2019_by_week: {}.'.format(number_of_rows))

# # - 2020 group
df_2020_by_week = df_2020_by_week.groupby(['WEEK_OF_YEAR']).sum()
print(df_2020_by_week)
number_of_rows = len(df_2020_by_week.index)
print('-- Row count of grouped df_2020_by_week: {}.'.format(number_of_rows))

df_by_week_merged = pd.merge(df_2020_by_week, df_2019_by_week, on='WEEK_OF_YEAR', how='outer')
number_of_rows = len(df_by_week_merged.index)
print('-- Row count of grouped df_by_week_merged: {}.'.format(number_of_rows))

# # - reset index to get the 'WEEK_OF_YEAR' back as a column
df_by_week_merged.reset_index(inplace=True)

print(' \n -- Columns names from df_by_week_merged:')
for col in df_by_week_merged.columns:
    print(col)

# #  - Dump unneeded columns
# df_by_week_merged = df_by_week_merged[['WEEK_OF_YEAR', 'EVENT_COUNT_2019_WEEKLY', 'FATALITIES_2019_WEEKLY',
# 'EVENT_COUNT_2020_WEEKLY', 'FATALITIES_2020_WEEKLY']]  # I can't get this to work.

# print(' \n -- Columns names from df_by_week_merged after dumping unneeded columns:')
# for col in df_by_week_merged.columns:
#     print(col)

# # - Write the by_week file to disk.
print('--- About to print: by_week_to_Matplotlib.CSV ')
df_by_week_merged.to_csv(r'C:\Users\Roger Helms\Documents\GitHub\final_project\by_week_to_Matplotlib.CSV')

print('end of script')

# # This stuff works in Jupyter, but not PyCharm
# #  - dump unneeded columns
# df_by_week_merged = df_by_week_merged[['EVENT_COUNT_2019_WEEKLY', 'FATALITIES_2019_WEEKLY','EVENT_COUNT_2020_WEEKLY','FATALITIES_2020_WEEKLY']]
#
# print(' ')
# print('-- Columns in df_by_week_merged after resetting index:')
# for col in df_by_week_merged.columns:
#     print(col)



