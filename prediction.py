import mysql.connector
import pymysql
import requests
import time
from pprint import pprint
from scipy import stats
from decimal import Decimal

mydb = mysql.connector.connect(
  host="database-2.csrajsjhoemp.us-east-1.rds.amazonaws.com",
  user="admin",
  database="bakalaurinis",
  password="bakalauras",
  port="3308")

cursor = mydb.cursor()
url = 'https://api.open-meteo.com/v1/forecast?latitude=54.69&longitude=25.28&hourly=windspeed_80m&windspeed_unit=ms&forecast_days=3'

result = requests.get(url)
data = result.json()
wind = data['hourly']['windspeed_80m']
date = data['hourly']['time']
x = [0,2.5,4,5,6,7,8,9,10,11,12,13,15]
y = [0.01,0.05,0.07,0.1,0.12,0.14,0.17,0.24,0.3,0.32,0.34,0.36,0.4]
output_array = []
slope, intercept, r, p, std_err = stats.linregress(x, y)
a=0.8

def myfunc(x):
  return slope * x * a + intercept 

for elementas in wind:
    result = myfunc(elementas)
    rounded = round(result,2)
    output_array.append(rounded)

print(output_array)
print(wind)

# Loop through each element in the arrays and insert them into the database
for i in range(len(wind)):
    # Convert the output_array value to Decimal format
    predicted_voltage = Decimal(str(output_array[i]))

    # Construct the SQL query
    query = "INSERT INTO prediction (Windspeed, Date, Predicted_voltage) VALUES (%s, %s, %s)"
    values = (wind[i], date[i], predicted_voltage)

    # Execute the query with the values as parameters
    cursor.execute(query, values)

# Commit the changes
mydb.commit()

# Close the cursor and connection
cursor.close()

import sys
import matplotlib
matplotlib.use('Agg')

import numpy
import matplotlib.pyplot as plt

x = [0,2.5,4,5,6,7,8,9,10,11,12,13,15]
y = [0.01,0.05,0.07,0.1,0.12,0.14,0.17,0.24,0.3,0.32,0.34,0.36,0.4]

mymodel = numpy.poly1d(numpy.polyfit(x, y, 3))

myline = numpy.linspace(1, 22, 100)

plt.scatter(x, y)
plt.plot(myline, mymodel(myline))
plt.show()

#Two  lines to make our compiler able to draw:
plt.savefig(sys.stdout.buffer)
sys.stdout.flush()

