import requests
import mysql.connector as mysql
from mysql.connector import Error

token = ""
try:
    conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                         password='sd5w2V!0')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS mmk_boats;')
        print('Creating table....')
        # in the below line please pass the create table statement which you want #to create
        cursor.execute("CREATE TABLE `user7313393746_booking`.`mmk_boats` ( `id` INT NOT NULL AUTO_INCREMENT , `boat_name` VARCHAR(255) , `boat_id` VARCHAR(255) NOT NULL , PRIMARY KEY (`id`))")
        print("Table Boat is created....")
        import requests

        reqUrl = "https://www.booking-manager.com/api/v2/yachts?companyId=2103"

        headersList = {
            "Accept": "*/*",
            "User-Agent": "Thunder Client (https://www.thunderclient.com)",
            "Authorization": "Bearer 837-d6973f84d9b2752274d9695ee411b01176871329d36b12872601a0837b390374104b7fa3542e0aefade6f65835bd09885f372592ddc57b44a2a853602dd03cc2"
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        import json
        print(type(response.text))
        boats = json.loads(response.text)
        mycursor = conn.cursor()
        for item in boats:
            print(item["name"])
            sql = "INSERT INTO mmk_boats (boat_name, boat_id) VALUES (%s, %s)"
            val = (item["name"], item["id"])
            mycursor.execute(sql, val)

            conn.commit()
except Error as e:
    print(e)