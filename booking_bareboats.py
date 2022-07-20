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
        cursor.execute('DROP TABLE IF EXISTS boats_booking;')
        cursor.execute(
        "CREATE TABLE `user7313393746_booking`.`boats_booking` ( `book_id` INT NOT NULL AUTO_INCREMENT , `boat_id` INT(11) NOT NULL , `status` INT(11) NOT NULL , `datestart` DATE , `dateend` DATE , `hash_dates` VARCHAR(255) , PRIMARY KEY (`book_id`))")
        print("Table Boat Bookings is created....")

        import requests
        reqUrl = "https://api.sednasystem.com/API/getaccess.asp?l=Zonepage&p=Zonepage2022@&appname=apiboatcharter"

        headersList = {
            "Accept": "*/*",
            "User-Agent": "opa36",
            "connection": "Keep-alive"
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        import xml.etree.ElementTree as ET

        xml = ET.fromstring(response.text)

        for holiday in xml.findall('token'):
            print(holiday.attrib['authtoken'])
            token = holiday.attrib['authtoken']



except Error as e:
    print(e)

payload = ""
mycursor = conn.cursor()


mycursor.execute('SELECT * FROM boats')
row_headers = [x[0] for x in mycursor.description] #this will extract row headers
rv = mycursor.fetchall()
for result in rv:



    reqUrl = "https://api.sednasystem.com/api/getBookingData.asp?api_mode=xml&appname=apiboatcharter&token=" + token + "&id_boat=" + str(result[2]) + "&date_start=2022-05-01&date_end=2022-12-31"
    payload_bo = ""
    response_bo = requests.request("GET", reqUrl, data=payload_bo, headers=headersList)
    import datetime as dt
    xml_bo = ET.fromstring(response_bo.text)
    for holiday_bo in xml_bo.findall('charter'):
        d_dateFrom = int(dt.datetime.strptime(holiday_bo.attrib['datestart'], "%Y-%m-%d").timestamp())

        # Convert datetime object to date object.

        d_dateTo = int(dt.datetime.strptime(holiday_bo.attrib['dateend'], "%Y-%m-%d").timestamp())


        sql = "INSERT INTO boats_booking (boat_id, status, datestart, dateend, hash_dates) VALUES (%s, %s, %s, %s, %s)"
        val = (result[2], holiday_bo.attrib['status'], holiday_bo.attrib['datestart'], holiday_bo.attrib['dateend'], (str(d_dateFrom + d_dateTo)))
        mycursor.execute(sql, val)
        conn.commit()