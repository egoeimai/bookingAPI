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
        cursor.execute('TRUNCATE TABLE boat_images;')
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
    images = boat.findall('picts')
    print(type(images))
    for pictures in images:
        images_inner = pictures.findall('pict')
        for pictures_inner in images_inner:
            print(pictures_inner.attrib['link'])
            sqls_images = "INSERT INTO `boat_images` (`boat_id`, `image_url`) VALUES (%s, %s);"
            images_vals = (boat.attrib['id_boat'], pictures_inner.attrib['link'])
            mycursor.execute(sqls_images, images_vals)
            conn.commit()
