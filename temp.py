import pandas as pd
import numpy as np
import datetime as dt

# Reading the csv file and storing in dataframe
meterReading_df = pd.read_csv("MeterReading_snippet.csv")

# Data wrangling - Part of the functionality might be processed in the previous step/recipe of Dataiku
# TODO: Analyze the impact on performance due the ordering/sequence of the column addition to the dataframe


# Declaring and initializing the panda dataframe
pandas_dataframe = pd.DataFrame()
pandas_dataframe = pandas_dataframe.fillna(0)


#df.pivot_table('time', ['Year', 'Country'], 'medal')
#"meterID","kwh","time","day"

trans = meterReading_df.pivot_table('kwh',['meterID','day'], 'time' )
print(trans)