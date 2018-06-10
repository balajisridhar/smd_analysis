import pandas as pd
import numpy as np
import datetime as dt

# Reading the csv file and storing in dataframe
meterReading_df = pd.read_csv("MeterReading.csv")

# Data wrangling - Part of the functionality might be processed in the previous step/recipe of Dataiku
# TODO: Analyze the impact on performance due the ordering/sequence of the column addition to the dataframe


# Declaring and initializing the panda dataframe
pandas_dataframe = pd.DataFrame()
pandas_dataframe = pandas_dataframe.fillna(0)

# Param 0
# This is to list the meter ID
meter_id = meterReading_df.groupby("meterID")['meterID'].mean()
pandas_dataframe["meterID"] = pd.Series(meter_id)

# To be used in future
no_of_days = meterReading_df.groupby("meterID")['day'].nunique()


# Param 1
# Computing the mean of kwh grouped by meterID
comp_mean = meterReading_df.groupby("meterID")['kwh'].mean()
pandas_dataframe["mean"] = pd.Series(comp_mean)

# Param 2
# TODO: ? what is the difference between the l and n paramter in paper
# To determine the maximum power consumption for a given meterID
max_consumption_df = meterReading_df.groupby("meterID").max()
max_consumption = max_consumption_df['kwh']
pandas_dataframe["max"] = pd.Series(max_consumption)

# Param 3
# Determining the cycle during which the maximum consumption occurs
max_cycle = max_consumption_df['time']
# Not the elegant way of identifying the cycle in which max power consumption occurs
# TODO: Update the function or find the better way of identifying the cycle
max_loc = meterReading_df.loc[meterReading_df.groupby(['meterID'])['kwh'].idxmax()]
toumax = max_loc.groupby("meterID")['time'].max()
pandas_dataframe["ToUmax"] = pd.Series(toumax)

# Param 4
# Determining the total electricity consumed over a period of time (0 to 48 interval)
tec = meterReading_df.groupby("meterID")['kwh'].sum()
pandas_dataframe["TEC"] = pd.Series(tec)

# Param 5
# Determining the mean daily max average of the max values
# This needs to be done in two step process for python 2.7 and panadas 0.18.1 version which is the
# supported version in dataiku
mdm_aggr = meterReading_df.groupby(["meterID", "day"])['kwh'].max()
mdm = mdm_aggr.groupby(level='meterID').mean()
pandas_dataframe["MDM"] = pd.Series(mdm)

# Param 6
# Determining the load factor for a give meterID
load_factor =  comp_mean / mdm
pandas_dataframe["LF"] = pd.Series(load_factor)

# Param 7
# Computing the variance of kwh grouped by meterID
comp_variance = meterReading_df.groupby("meterID")['kwh'].var()
pandas_dataframe["Var"] = pd.Series(comp_variance)

# Param 8
# Computing the standard deviation of kwh grouped by meterID
comp_std = meterReading_df.groupby("meterID")['kwh'].std()
pandas_dataframe["SD"] = pd.Series(comp_std)

# Param 9
# Computing the consumption range of the given meterID
# Computing the minimum power consumed for given meterID
min_consumption_df = meterReading_df.groupby("meterID").min()
consumption_range = max_consumption_df - min_consumption_df
pandas_dataframe["Range"] = pd.Series(consumption_range['kwh'])

# Param 10
# Calculate the Inter Quaratile Range IQR
# determine the first quaratile
quaratile_q1 = meterReading_df.groupby(["meterID"]).quantile(0.25)
quaratile_q3 = meterReading_df.groupby(["meterID"]).quantile(0.75)
iqr = quaratile_q3 - quaratile_q1
pandas_dataframe["IQR"] = iqr['kwh']

# Compute the week day list, assuming the year to be 2008
week_days = []
start_date = dt.datetime(2008,01,01)
for day in range(195,366):
    curr_date = start_date + dt.timedelta(days = day)
    # print(curr_date.isoweekday() in range(1,6))
    if(curr_date.isoweekday() in range(1,6)):
        week_days.append(day)
#print(week_days)

# Param 11
# Determining the Morning max
# Two step process 1) a) Filter the rows based on the range on the timings
# 1) b) Group the readings based on the meterID
morning_max_range = meterReading_df[(meterReading_df['time'].between(1,20,inclusive=True)& meterReading_df['day'].isin(week_days))].groupby(['meterID','day'])['kwh'].max()
# 2) compute the average grouping by meterID
print(morning_max_range)
morning_max = morning_max_range.groupby(level='meterID').mean()
pandas_dataframe["MORNMAX"] = pd.Series(morning_max)

# Param 12
# Compute the morning peak - difference between the MORNMAX and Morning Mean
# Two step process 1) Compute the morning mean

morning_mean = meterReading_df[(meterReading_df['time'].between(1,20,inclusive=True)& meterReading_df['day'].isin(week_days))].groupby(['meterID'])['kwh'].mean()
morning_peak = pd.Series(morning_max).subtract(morning_mean)
pandas_dataframe['MORNPEAK'] = pd.Series(morning_peak)

# Param 13
# TODO: ? would the Morning range calculaiton based on the minimum or mean minimum.
# Calculating the Morning range based on the mean minimum before 10AM

# Determining the Morning min
# Two step process 1) a) Filter the rows based on the range on the timings
# 1) b) Group the readings based on the meterID
morning_min = meterReading_df[meterReading_df['time'].between(1,20,inclusive=True)].groupby(['meterID'])['kwh'].min()
morning_max = meterReading_df[meterReading_df['time'].between(1,20,inclusive=True)].groupby(['meterID'])['kwh'].max()
# 2) compute the average grouping by meterID
morning_range = morning_max - morning_min
pandas_dataframe["MORNRANGE"] = pd.Series(morning_range)



print("New aggregated values")
print(pandas_dataframe)



