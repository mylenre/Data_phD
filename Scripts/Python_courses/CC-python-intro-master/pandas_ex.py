# When to use pandas:
  # Table-like columnar data
  # Interfacing with databases (MySQL etc.)
  # Multiple data-types in a single data file.
# When not to use pandas:
  # For really simple data files (a single column of values in a text file, for example, might be overkill).
  # If you are dealing with large gridded datasets of a single data type --> numpy.
  # If you are doing lots of matrix calculations, or other heavily mathematical operations on gridded data --> numpy

import pandas as pd

data = pd.read_csv('StormEleanor_2_3_Jan.csv', delimiter=',', header=0)
print(type(data))

pressure_data = data['Pair_Avg']
print(pressure_data)
