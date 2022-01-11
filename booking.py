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
        cursor.execute('DROP TABLE IF EXISTS boats;')
        cursor.execute('DROP TABLE IF EXISTS boats_booking;')
        cursor.execute('DROP TABLE IF EXISTS boats_extras;')
        print('Creating table....')
        # in the below line please pass the create table statement which you want #to create
        cursor.execute("CREATE TABLE `user7313393746_booking`.`boats` ( `id` INT NOT NULL AUTO_INCREMENT , `boat_name` VARCHAR(255) , `boat_id` INT(11) NOT NULL , PRIMARY KEY (`id`))")
        print("Table Boat is created....")

        cursor.execute(
            "CREATE TABLE `user7313393746_booking`.`boats_extras` (`id` INT NOT NULL AUTO_INCREMENT, `id_opt` INT(11) NOT NULL, `id_opt_bt` INT(11) NOT NULL, `name` VARCHAR(255), `price` FLOAT(11) NOT NULL , `per` VARCHAR(255), `boat_id` INT(11) NOT NULL, PRIMARY KEY (`id`))")
        print("Table Boat EXTRAS is created....")

        cursor.execute(
            "CREATE TABLE `user7313393746_booking`.`boats_booking` ( `book_id` INT NOT NULL AUTO_INCREMENT , `boat_id` INT(11) NOT NULL , `status` INT(11) NOT NULL , `datestart` VARCHAR(255) , `dateend` VARCHAR(255) , PRIMARY KEY (`book_id`))")
        print("Table Boat Bookings is created....")

        import requests

        reqUrl = "https://demoft.sednasystem.com/API/getaccess.asp?l=demoapifleet&p=demoapifleet&appname=apiboatcharter"

        headersList = {
            "Accept": "*/*",
            "User-Agent": "opa36",
            "connection": "Keep-alive"
        }

        payload = ""

        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        import xml.etree.ElementTree as ET

        xml = ET.fromstring(response.text)
        token = xml
        print(token)


except Error as e:
    print(e)

reqUrl = "https://demoft.sednasystem.com/API/getBts5.asp?token=x8gti2mjr9dk7o9y4o333y1am7wx5hrp1641900210251&appname=apiboatcharter"

headersList = {
 "Accept": "*/*",
 "User-Agent": "opa36",
 "connection": "Keep-alive"
}

payload = ""
mycursor = conn.cursor()
response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
import xml.etree.ElementTree as ET
xml=ET.fromstring(response.text)
for holiday in xml.findall('boat'):


    sql = "INSERT INTO boats (boat_name, boat_id) VALUES (%s, %s)"
    val = (holiday.attrib['name'], holiday.attrib['id_boat'])
    mycursor.execute(sql, val)

    conn.commit()

    print(mycursor.rowcount, "record inserted.")

mycursor.execute('SELECT * FROM boats')
row_headers = [x[0] for x in mycursor.description] #this will extract row headers
rv = mycursor.fetchall()
for result in rv:

    reqUrl = "https://demoft.sednasystem.com/api/getBookingData.asp?api_mode=xml&appname=apiboatcharter&token=x8gti2mjr9dk7o9y4o333y1am7wx5hrp1641900210251&id_boat="+ str(result[2]) +"&date_start=2018-01-01&date_end=2018-08-08"

    headersList = {
        "Accept": "*/*",
        "User-Agent": "opa36",
        "connection": "Keep-alive"
    }

    payload_bo = ""
    response_bo = requests.request("GET", reqUrl, data=payload_bo, headers=headersList)
    xml_bo = ET.fromstring(response_bo.text)
    for holiday_bo in xml_bo.findall('charter'):
        sql = "INSERT INTO boats_booking (boat_id, status, datestart, dateend) VALUES (%s, %s, %s, %s)"
        val = (result[2], holiday_bo.attrib['status'], holiday_bo.attrib['datestart'], holiday_bo.attrib['dateend'])
        mycursor.execute(sql, val)

        conn.commit()

    extras_url = "https://demoft.sednasystem.com/API/getExtras3.asp?id_boat="+ str(result[2]) +"&refope=demo36"

    payload_extras = ""
    response_extras = requests.request("GET", extras_url, data=payload_extras, headers=headersList)

    xml_extras = ET.fromstring(response_extras.text)

    for holiday_extras in xml_extras.findall('extra'):
        print(result[2])
        sql_extras = "INSERT INTO `boats_extras` (`id_opt`, `id_opt_bt`, `name`, `price`, `per`, `boat_id`) VALUES (%s, %s, %s, %s, %s, %s);"
        val_extras = (holiday_extras.attrib['id_opt'], holiday_extras.attrib['id_opt_bt'], holiday_extras.attrib['name'], holiday_extras.attrib['price'], holiday_extras.attrib['per'], result[2])
        mycursor.execute(sql_extras, val_extras)

        conn.commit()



