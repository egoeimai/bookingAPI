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
        cursor.execute('TRUNCATE TABLE boats;')
        cursor.execute('TRUNCATE TABLE boats_bases;')
        cursor.execute('TRUNCATE TABLE boat_characteristics;')
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
        for boat in xml.findall('token'):
            print(boat.attrib['authtoken'])
            token = boat.attrib['authtoken']
except Error as e:
    print(e)

reqUrl = "https://api.sednasystem.com/API/getBts5.asp?token=" + token + "&appname=apiboatcharter"

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


for boat in xml.findall('boat'):
    sql = "INSERT INTO boats (boat_name, boat_id) VALUES (%s, %s)"
    val = (boat.attrib['name'], boat.attrib['id_boat'])
    mycursor.execute(sql, val)
    conn.commit()
    print(mycursor.rowcount, "record inserted.")
    sqls = "INSERT INTO `boat_characteristics` (`boat_id`, `bt_type`, `crew`, `model`, `widthboat`, `nbdoucabin`, `nbsimcabin`, `nbper`, `nbbathroom`, `buildyear`, `std_model`, `builder`, `widthboat_feet`, `bt_comment`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    vals = (boat.attrib['id_boat'], boat.attrib['bt_type'], boat.attrib['crew'], boat.attrib['model'], boat.attrib['widthboat'], boat.attrib['nbdoucabin'], boat.attrib['nbsimcabin'], boat.attrib['nbper'], boat.attrib['nbbathroom'], boat.attrib['buildyear'], boat.attrib['std_model'], boat.attrib['builder'], boat.attrib['widthboat_feet'], boat.attrib['bt_comment'])
    mycursor.execute(sqls, vals)

    homeports = boat.findall('homeport')
    for homeport in homeports:
        sql_bases = "INSERT INTO boats_bases (boat_id, destination_id, destination_name, id_tbf1) VALUES (%s, %s, %s, %s)"
        val_bases = (
        boat.attrib['id_boat'], homeport.attrib['id_base'], homeport.attrib['name'], homeport.attrib['id_tbf1'])
        mycursor.execute(sql_bases, val_bases)

    conn.commit()

