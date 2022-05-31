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
        cursor.execute('TRUNCATE TABLE boat_characteristics_bare;')
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
with open("output.xml", "w") as f:
    f.write(response.text)
for boat in xml.findall('boat'):

    plans = boat.findall('plans')
    for  plan in  plans:
        for plan_inner in plan:
            print(plan_inner)
            sqls_plans = "INSERT INTO `bare_boat_plans` (`boat_id`, `plan_url`) VALUES (%s, %s);"
            plans_vals = (
            boat.attrib['id_boat'], plan_inner.attrib['link'])
            mycursor.execute(sqls_plans,  plans_vals)
            conn.commit()