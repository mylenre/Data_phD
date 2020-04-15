pressure_data = []

#weatherfile = open("StormEleanor_2_3_Jan.csv", "r")
#for line in weatherfile:
#  print(line)
#weatherfile.close()

with open("StormEleanor_2_3_Jan.csv", "r") as weatherfile:
  next(weatherfile) # to skip the head line
  for line in weatherfile:
    #print(line)
    #print(type(line))
    data_row = line.split(',')
    #print(line.split(','))
    pressure = data_row[6] # each value of pressure of line(i) is overwritten by the line(i+1) one 
    #print(pressure) # those are strings
    pressure_data.append(float(pressure)) # to store all pressure values in numerical format

print(pressure_data[0])
print(type(pressure_data[0]))
