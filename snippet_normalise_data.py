# Normalize time series dat
import pandas as ps
import sklearn as sk
from pandas import Series
from sklearn.preprocessing import MinMaxScaler
# load the dataset and print the first 5 rows
#series = Series.from_csv('data/daily-minimum-temperatures-in-me.csv', header=0, infer_datetime_format= True)
series = ps.read_csv('data/daily-minimum-temperatures-in-me.csv', header=0, infer_datetime_format= True)
print("Series of Head \n",series)
# prepare data for normalization
values = series.values

min_max_scaler = sk.preprocessing.MinMaxScaler()

normalized_data = series

# Normalizing the power consumption columns


x = series[['Daily minimum2']]

print("Selected values \n ",x)
dx = min_max_scaler.fit_transform(x)
norm_dx = ps.DataFrame(dx)


print("Normalized column\n",norm_dx)

normalized_data[['Daily minimum2']] = norm_dx

print("Normalized Data set \n", normalized_data)

#Assigning normalized column values to dataframe


# print(values.shape)
# print(values)
# print("-------------------------------------------")
#
#
# x_scaled = min_max_scaler.fit_transform(values)
# df = ps.DataFrame(x_scaled)
#
# print(df)



#
# values = values.reshape((len(values), 3))
# print(values.shape)
# print("BP 2", values)
# # train the normalization
# scaler = MinMaxScaler(feature_range=(0, 1))
# scaler = scaler.fit(values)
# print('Min: %f, Max: %f' % (scaler.data_min_, scaler.data_max_))
# print("-------------------------------------------")
# # normalize the dataset and print the first 5 rows
# normalized = scaler.transform(values)
# print(normalized)
#
# for i in range(5):
# 	print(normalized[i])
# # inverse transform and print the first 5 rows
# print("-------------------------------------------")
# inversed = scaler.inverse_transform(normalized)
# print(inversed)
# for i in range(5):
# 	print(inversed[i])