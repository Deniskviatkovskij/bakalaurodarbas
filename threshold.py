from decimal import Decimal
import mysql.connector
import time

def connect_to_database():
    # connect to the database
    mydb = mysql.connector.connect(
        host="database-2.csrajsjhoemp.us-east-1.rds.amazonaws.com",
        user="admin",
        database="bakalaurinis",
        password="bakalauras",
        port="3308"
    )
    return mydb

def update_data():
    while True:
        try:
            mydb = connect_to_database()
            cursor = mydb.cursor()

            latest_threshold = "SELECT temperature_max FROM dashboard_thresholds WHERE id=1"
            cursor.execute(latest_threshold)
            result = cursor.fetchone()
            temperature_max = result[0]
            print("Temperature max value:", temperature_max)

            latest_voltage = "SELECT Power FROM layout_data ORDER BY ID DESC LIMIT 1"
            cursor.execute(latest_voltage)
            result = cursor.fetchone()
            latest_voltage = result[0]
            print("Latest voltage value:", latest_voltage)

            latest_temperature = "SELECT Temperature FROM layout_data ORDER BY ID DESC LIMIT 1"
            cursor.execute(latest_temperature)
            result = cursor.fetchone()
            latest_temperature = result[0]
            print("Latest temperature value:", latest_temperature)

            if latest_temperature > temperature_max:
                update_query = "UPDATE layout_data SET Power = %s WHERE id = (SELECT * FROM (SELECT id FROM layout_data ORDER BY id DESC LIMIT 1) as subquery) AND %s > (SELECT temperature_max FROM dashboard_thresholds WHERE id = 1)"
                cursor.execute(update_query, (Decimal('0'), latest_temperature))
                mydb.commit()
                print("Power updated successfully")
            else:
                print("No update needed")
            
            cursor.close()
            mydb.close()

        except mysql.connector.Error as error:
            print("Error while connecting to MySQL:", error)
            print("Retrying in 5 seconds...")
            time.sleep(5)
        
        time.sleep(2) # Pause the execution for 5 seconds before the next iteration

update_data()
