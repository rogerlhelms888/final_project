# # - This script file's path:
# # -     C:\Users\Roger Helms\Documents\GitHub\final_project\ACLED_to_map_PROD.py
# # - Stored in this remote GitHub repo: https://github.com/rogerlhelms888/final_project
# # - Stored in this local Github repo:  C:\Users\Roger Helms\Documents\GitHub\final_project

# # - The overall object of the project is to automate the creation of bar charts and interactive maps based on a
# # -     listing of 'confict' events maintained by the aggregator ACLED.
# # - This is the first of three files.
# # -     1) This script creates two CSV files used to create bar charts.
# # -     2) The next script plots those bar charts.
# # -        C:\Users\Roger Helms\Documents\GitHub\final_project\ACLED_bar_chart.py
# # -     3) The final script creates a CSV file of coordinates to be mapped in ArcGIS Online.
# # -        C:\Users\Roger Helms\Documents\GitHub\final_project\ACLED_to_map_DEV.py
# # - Data Source.  The data comes as an XLSX table from the Central Asia & the Caucuses section of ACLED's
# # -       'Curated Data Files' page: https://acleddata.com/curated-data-files/
# # -       URL of the download button at 5/1/20:  https://acleddata.com/download/18750/  It doesn't change.
# # -       Excel file example at 5/1/20:
# # -       C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\CCA_2017-2020_Apr25.xlsx
# # -       https://acleddata.com/download/18750/
# # - Output:
# # -       - a CSV of event counts and fatalities by day:           by_day_to_Matplotlib.CSV
# # -       - a CSV of event counts and fatalities by week:          by_week_to_Matplotlib.CSV
# # -       (a third CSV of coordinates to map is created in a subsequent script).

# # - IMPORT methods
import datetime as dt
import pandas as pd
import numpy as np
from IPython.display import IFrame
import matplotlib.pyplot as plt
import missingno as msno
import seaborn as sns
import math as math
import requests  # used to download the ACLED XLSX to my C:\


# # configure PyCharm to see more columns across more of the screen than the default permits.
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)

# # Open the ACLED curated XLSX file for 'Central Asia & the Caucuses'.
# # ACLED's webpage is: https://acleddata.com/curated-data-files/
url = 'https://acleddata.com/download/18750/'
ACLED_latest_Excel = requests.get(url)
open(r'C:\Users\Roger Helms\Documents\GitHub\final_project\ACLED_latest_Excel.xlsx', 'wb')\
    .write(ACLED_latest_Excel.content)
df = pd.read_excel(r'C:\Users\Roger Helms\Documents\GitHub\final_project\ACLED_latest_Excel.xlsx')
# # - display the newly created dataframe
# print(df.head())

# # - Capture the current dataframe's columns' names as a list for later comparison to the expected ones:
current_ACLED_cols = []
for my_col in df.columns:
    current_ACLED_cols.append(my_col)
# print('current_ACLED_cols:\n {}'.format(current_ACLED_cols))

# # Expected column names as of 5/6/20.  PRESERVE for reference in case of problems later.
# # -  ['ISO', 'EVENT_ID_CNTY', 'EVENT_ID_NO_CNTY', 'EVENT_DATE', 'YEAR', 'TIME_PRECISION', 'EVENT_TYPE',
# # -   'SUB_EVENT_TYPE', 'ACTOR1', 'ASSOC_ACTOR_1', 'INTER1', 'ACTOR2', 'ASSOC_ACTOR_2', 'INTER2', 'INTERACTION',
# # -   'REGION', 'COUNTRY', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION', 'LATITUDE', 'LONGITUDE', 'GEO_PRECISION',
# # -   'SOURCE', 'SOURCE_SCALE', 'NOTES', 'FATALITIES', 'TIMESTAMP']

# # - CONTROL.  Did we get the columns we expect from the newly read CSV file?
# # -    Compare the expected column names (from May 2 2020) to the 'read' ones of the latest ACLED curated file.
original_ACLED_cols = ['ISO', 'EVENT_ID_CNTY', 'EVENT_ID_NO_CNTY', 'EVENT_DATE', 'YEAR', 'TIME_PRECISION',
                       'EVENT_TYPE', 'SUB_EVENT_TYPE', 'ACTOR1', 'ASSOC_ACTOR_1', 'INTER1', 'ACTOR2', 'ASSOC_ACTOR_2',
                       'INTER2', 'INTERACTION', 'REGION', 'COUNTRY', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION',
                       'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', 'SOURCE', 'SOURCE_SCALE', 'NOTES', 'FATALITIES',
                       'TIMESTAMP']
if current_ACLED_cols == original_ACLED_cols:
    print('OK. We got the columns we expected from ACLEDs curated XSLX file')
elif current_ACLED_cols != original_ACLED_cols:
    print('ERROR: The newly loaded columns are not as expected.')
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

# # - Control.  Are there any records outside of the expected range of dates?
# # - Earliest Date.  The earliest expected date will probably never change if we're only dealing with Afghan records.
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
# # - Next row normally commented during DEV (it's a pain to input for testing) and uncommented during production.
#   latest_date_as_input = input ("  ! ENTER the year, month, and day, like : " '25 April 2020') # Used in PROD
latest_date_as_input = '9 May 2020'  # Used in DEV.

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

# # - Stop the script if the earliest date is not as expected.
if earliest_actual_date != earliest_expected_date:
    raise Exception('EXCEPTION.  The earliest ACTUAL date was not the same as the earliest EXPECTED date: {}'
                    .format(earliest_expected_date))  # Tested and correctly raised an exception.
# # - Stop the script if the latest date is not as expected.
if latest_actual_date != latest_expected_date:
    raise Exception('EXCEPTION.  The last ACTUAL date was not the same as the last EXPECTED date: {}'
                    .format(latest_expected_date))  # Tested and correctly raised an exception.

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
df = df[['EVENT_ID_CNTY', 'EVENT_DATE', 'EVENT_DATE_NUM', 'TIME_PRECISION', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'ACTOR1',
         'ACTOR2', 'ADMIN1', 'ADMIN2', 'ADMIN3', 'LOCATION', 'LATITUDE', 'LONGITUDE', 'GEO_PRECISION', 'SOURCE',
         'SOURCE_SCALE', 'FATALITIES']]

# # REVIEW
number_of_rows = len(df.index)
print('row count of all individual events after dropping non-violent events: {}.'.format(number_of_rows))

# # - Filter down to the period 1/1/19 to date.
df = df[df['EVENT_DATE_NUM'] >= pd.to_datetime('1 January 2019')]
number_of_rows = len(df.index)
print('row count after dropping first two years: {}.'.format(number_of_rows))
# # - 16096  3,120 KB on 25 April 2020 version.

print('The last date in the table as downloaded:')
print(df['EVENT_DATE_NUM'].tail(1))  # We now expect to see the last day of ACLED's most recent update.
# # - Eliminate the records for the last day.
df = df[df['EVENT_DATE_NUM'] != pd.to_datetime(latest_date_as_input)]
print('The last date in the table after deleting the last day of the reporting period:')
print(df['EVENT_DATE_NUM'].tail(1))  # We now don't expect to see that anemic last day of ACLED's data.

# # - Save a copy of the dataframe as filtered for later use in separate script to prepare a file to be mapped.
# # - That separate script is:
# # -    C:\Users\Roger Helms\Documents\GitHub\final_project\ACLED_to_map_DEV.py
df.to_csv(r'C:\Users\Roger Helms\Documents\GitHub\final_project\df_filtered.csv')

# # GROUP for reporting by day.
# - Add an EVENT_COUNT column of 1's to permit summing.
df['EVENT_COUNT'] = 1

# - Populate a new column with the dayofyear (eg. Jan 1 = 1, Jan 2 = 2... Feb 1 = 32...)
df['DAY_OF_YEAR'] = df['EVENT_DATE_NUM'].dt.dayofyear # <<<
print('df before grouping:')
print(df)

# WRONG!  WE'RE grouping too early and losing our 'DAY_OF_YEAR' column.
# # - Group by day (NOT by day of year) and sum numeric columns.
# df_by_day = df.groupby(['EVENT_DATE_NUM']).sum()
# print(df_by_day)
# number_of_rows = len(df_by_day.index)
# Print('row count of both years combined, grouped by day (NOT day of year): {}.'.format(number_of_rows))

# # - Dump useless cols (like lats and longs) from df_by_day.
# df_by_day = df[['FATALITIES', 'EVENT_COUNT','DAY_OF_YEAR']]
# print('-- df_by_day after dumping useless columns')
# print(df_by_day)

# - Get the EVENT_DATE_NUM index back as a column.
# df_by_day.reset_index(inplace=True)
# print('-- df_by_day after reseting index')
# print(df_by_day)

# # - Now establish columns for FATALITIES and for EVENT_COUNT for each year, so it looks like this:

# # - DAY_OF_YEAR     FATALITIES_2020  EVENT_COUNTS_2020   FATALITIES_2019  EVENT_COUNTS_2019...
# # - 1               123                44                154                 33
# # - 2               123                40                135                 30

# # - Do this by creating a series of integers 1-366 days and merging it to
# # -    extracts of the df_by_day dataframe for 2020 and, separately, for 2019.
# # -    The join would be on the DAY_OF_YEAR values.

# # - Copy out the 2019 records into their own dataframe, then rename their columns
df_2019 = df[df['EVENT_DATE_NUM'] >= pd.to_datetime('1 January 2019')] # <<<
df_2019 = df[df['EVENT_DATE_NUM'] < pd.to_datetime('1 January 2020')]
# # - Rename columns to distinguish the two columns so they will merge as distinct columns.
df_2019.rename(columns={'FATALITIES': 'FATALITIES_2019'}, inplace=True)
df_2019.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2019'}, inplace=True)
df_2019.reset_index(inplace=True) # <<<
print('--- Here is 2019 before grouping:')
print(df_2019[['EVENT_DATE_NUM', 'EVENT_COUNT_2019', 'DAY_OF_YEAR']])
# print(df_2019)
number_of_rows = len(df_2019.index)
print('row count of df_2019: {}.'.format(number_of_rows))

# # - Group 2019 by day (NOT by day of year) and sum numeric columns.
df_2019_grouped = df_2019.groupby(['DAY_OF_YEAR']).sum()
# print(df_2019)
# print(df_2019_grouped[['EVENT_DATE_NUM', 'FATALITIES_2020', 'EVENT_COUNT_2020', 'DAY_OF_YEAR']])
number_of_rows = len(df_2019_grouped.index)
print('row count of df_2019, grouped by day (NOT day of year): {}.'.format(number_of_rows))

# # Copy out the 2020 records into their own dataframe, then rename their columns
df_2020 = df[df['EVENT_DATE_NUM'] >= pd.to_datetime('1 January 2020')]
df_2020 = df[df['EVENT_DATE_NUM'] < pd.to_datetime('1 January 2021')]
# # - Rename columns to distinguish the two columns so they will merge as distinct columns.
df_2020.rename(columns={'FATALITIES': 'FATALITIES_2020'}, inplace=True)
df_2020.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2020'}, inplace=True)
df_2020.reset_index(inplace=True) # <<<
print('--- Here is the extract for 2020, not yet grouped:')
print(df_2020[['EVENT_DATE_NUM', 'FATALITIES_2020', 'EVENT_COUNT_2020', 'DAY_OF_YEAR']])
# print(df_2020)
number_of_rows = len(df_2020.index)
print('row count of df_2020, which has not yet been grouped: {}.'.format(number_of_rows))

# # - Group 2020 by day (NOT by day of year) and sum numeric columns.
df_2020_grouped = df_2020.groupby(['DAY_OF_YEAR']).sum()
print(df_2020_grouped)
number_of_rows = len(df_2020_grouped.index)
# Print('row count of both years combined, grouped by day (NOT day of year): {}.'.format(number_of_rows))

# # - We don't use 2018 or 2017 so far, for want of interest.  We have the data and could.

# # - Create a two column dataframe of integers 1-366 to use in merges.  We need this
# # - because we don't have events for every day (two days were missing in 2019), and will need every day,
# # - populated or not, for the bar charts. 2020 was a leap year with 366 days.
all_days_list = []
num_list = range(1, 367, 1)
for num in num_list:
    all_days_list.append(num)

print('--- all_days_list')
print(all_days_list)

df_all_days = pd.DataFrame({
    'DAY_OF_YEAR': all_days_list
})
print('--- df_all_days:')
print(df_all_days)

# # - Merge the list of 366 and the 2020 lists.
df_2020 = pd.merge(df_all_days, df_2020_grouped, on='DAY_OF_YEAR', how='outer')
print('\n --- We just merged df_all_days, with 366 records, and df_2020_grouped with .  In the new df_2020, we expect'
      'as many rows as in the original df_2020, plus some for the future days'
      'of 2020 for which we had no records in the original table.  About 240 at writing.')
number_of_rows = len(df_2020.index)
print('row count of df_2020 which has been merged with the df_all_days list of 366 days: {}.'.format(number_of_rows))

# # - Merge 2019 and 2020 by day into a single table using an outer join.
df_merged = pd.merge(df_2020_grouped, df_2019_grouped, on='DAY_OF_YEAR', how='outer')
# # print(df_merged[['EVENT_DATE_NUM', 'EVENT_COUNT_2019', 'FATALITIES_2019', 'EVENT_COUNT_2020', 'FATALITIES_2020']])
number_of_rows = len(df_2020.index)
print('---Row count of merged df_all_days, df_2019, df_2020 by day. There s/b 366 rows: {}.'.format(number_of_rows))

# -------- checked in Jupyter till here




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

# Copy out the 2019 records into their own dataframe, then rename their columns
df_2019_by_week = df[df['EVENT_DATE_NUM'] >= pd.to_datetime('1 January 2019')]
df_2019_by_week = df[df['EVENT_DATE_NUM'] < pd.to_datetime('1 January 2020')]
df_2019_by_week.rename(columns={'FATALITIES': 'FATALITIES_2019_WEEKLY'}, inplace=True)
df_2019_by_week.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2019_WEEKLY'}, inplace=True)
print('The FATALITIES_2019_WEEKLY and EVENT_COUNT_2019_WEEKLY columns are just placeholders so far:')
# print(df_2019_by_week[['EVENT_DATE_NUM', 'FATALITIES_2019_WEEKLY', 'EVENT_COUNT_2019_WEEKLY', 'DAY_OF_YEAR',
# 'WEEK_OF_YEAR']])

# Copy out the 2019 records into their own dataframe, then rename their columns
df_2020_by_week = df[df['EVENT_DATE_NUM'] >= pd.to_datetime('1 January 2020')]
df_2020_by_week = df[df['EVENT_DATE_NUM'] < pd.to_datetime('1 January 2021')]
df_2020_by_week.rename(columns={'FATALITIES': 'FATALITIES_2020_WEEKLY'}, inplace=True)
df_2020_by_week.rename(columns={'EVENT_COUNT': 'EVENT_COUNT_2020_WEEKLY'}, inplace=True)
print('The FATALITIES_2020_WEEKLY and EVENT_COUNT_2020_WEEKLY columns are just placeholders so far:')
# print(df_2020_by_week[['EVENT_DATE_NUM', 'FATALITIES_2020_WEEKLY', 'EVENT_COUNT_2020_WEEKLY', 'DAY_OF_YEAR',
# 'WEEK_OF_YEAR']])

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
print('\n --- About to print: by_week_to_Matplotlib.CSV ')
df_by_week_merged.to_csv(r'C:\Users\Roger Helms\Documents\GitHub\final_project\by_week_to_Matplotlib.CSV')


print('The next script will plot the two CSVs that were just created.  It is:')
print('C:_Users_Roger Helms_Documents_GitHub_final_project_ACLED_bar_chart.py')

print('\n End of script')