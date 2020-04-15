import csv

pressure_data = []   # Create an empty list as before to store values

with open('StormEleanor_2_3_Jan.csv', 'r') as csvfile:
  next(csvfile)
  for row in csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC): #quoting=csv.QUOTE_NONNUMERIC tells the csv module to read all the non-quoted values in the csv file as strings, and the rest as numeric values (e.g. floats)
    pressure_data.append(row[6])

# Check our variables look okay and they are the correct type:
print(pressure_data)
print(type(pressure_data[1]))
