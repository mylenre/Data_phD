# import the required libraries and modules
import datetime
import pandas as pd
import matplotlib.pyplot as plt

# Code to create the timeseries values
date_time_series = []
date_time = datetime.datetime(2018, 1, 2)
date_at_end = datetime.datetime(2018, 1, 3, 23, 59)
step = datetime.timedelta(minutes=1)

while date_time <= date_at_end:
  date_time_series.append(date_time)
  date_time += step

print(date_time_series)

# import and plot data 

data = pd.read_csv('StormEleanor_2_3_Jan.csv', delimiter=',', header=0)

pressure_data = data['Pair_Avg']

#plt.plot(pressure_data)
#plt.title("Average Pressure, JCMB Weather Station, 2-3rd Jan 2018")
#plt.savefig("pressure.png")

plt.plot(date_time_series, pressure_data)
plt.ylabel("Pressure (hPa)")
plt.xlabel("Time")
plt.title("Average Pressure, JCMB Weather Station, 2-3rd Jan 2018")
plt.xticks(rotation=-60)
plt.tight_layout()
plt.savefig("pressure_final.png")
