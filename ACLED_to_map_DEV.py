# # - Roger Helms' capstone project to automate ACLED reporting TO MAP.
# # -     (There is also a TO GRAPH script that creates a CSV used below.
# # -      C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\ACLED_to_graph_DEV.py).
# # - This file's path, working directory and remote Github repo (a/o 5/1/20):
# # -     C:\Users\Roger Helms\Documents\GitHub\pratt-savi-810-2020-03-activity_01\maps\ACLED_to_map_DEV.py
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
# # -  Conventions:
# # -            # # -  for lines of pure annotation, with nothing to run.
# # -            #      for 'commented' code that could run.
# # -            <<<    a flag for me to address some hanging issue

import datetime
import pandas as pd
import numpy as np

# # - Create a dataframe from a CSV prepared earlier using the script ACLED_to_graph_DEV.
# # -    The current one is for 1/1/19 thru 4/25/20 as of 5/1/20 for Afghanistan only, and violent events only
# # -    (Only battles, remote violence and violence against civilians.  No strategic developments or riots.)


# - Read in the filtered file
df = pd.read_csv('df_filtered.csv')
number_of_rows = len(df.index)
print('row count of reopened df_filtered.csv: {}.  (S/B the same at 5/4/20.)'.format(number_of_rows))

print(df[['LATITUDE','LONGITUDE']])

# - add an EVENT_COUNT column of 1's to permit summing to day counts or week counts.
df['EVENT_COUNT'] = 1

for col in df.columns:
    print(col)

    # EVENT_ID_CNTY
    # EVENT_DATE
    # EVENT_DATE_NUM
    # TIME_PRECISION
    # EVENT_TYPE
    # SUB_EVENT_TYPE
    # ACTOR1
    # ACTOR2
    # ADMIN1
    # ADMIN2
    # ADMIN3
    # LOCATION
    # LATITUDE
    # LONGITUDE
    # GEO_PRECISION
    # SOURCE
    # SOURCE_SCALE
    # FATALITIES
    # EVENT_COUNT
    # COORD_STRING

print('Type of df after adding EVENT_COUNT column: {}'.format(type(df)))

# # - Filter out records with geoprecision of 3.  (3 = Defaulted to the provincial capital.)
df = df[(df.GEO_PRECISION)<3]

# # - Review
number_of_rows = len(df.index)
print('row count after dropping GEO_PRECISION of 3, (default to prov. cap.) : {}.'.format(number_of_rows))
# The count shows a decrease, so we should be good.

# - add a column to receive a concatenation of the LATITUDE and LONGITUDE for later grouping.
df['COORD_STRING'] = str(df.LATITUDE)+" "+str(df.LONGITUDE)  # <<< runs, but the result is strange
# # so I'm going to punt by grouping on latitude + district name, which is a little goofy and risky <<<<

# print(df[['LATITUDE','LONGITUDE','COORD_STRING']])
print(" # print(df[['LATITUDE','LONGITUDE','COORD_STRING']])")
print(df['COORD_STRING'])

# # - Group by coordinates.  (Most events are coded to district centers, which are the same exact lat-longs.)
df_by_coord = df.groupby(['COORD_STRING']).sum()
# print(df_by_coord[['COORD_STRING','FATALITIES','EVENT_COUNT']])

print(df_by_coord.head())
#  df_by_day = df.groupby(['EVENT_DATE_NUM']).sum() # <<<


# for item in df.GEO_PRECISION:
#     print(item)


