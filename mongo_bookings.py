from pymongo import MongoClient
import mysql.connector as mysql
from mysql.connector import Error
import hashlib
import json

token = ""
try:
    conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                         password='sd5w2V!0')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)



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

try:
    client = MongoClient(
        "mongodb+srv://yachting_solutions:NCJ7mtjQLjqf9ez1@crewed.631yzli.mongodb.net/?retryWrites=true&w=majority")

    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")
payload = ""
mycursor = conn.cursor()

mycursor.execute('SELECT * FROM boats')
row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
rv = mycursor.fetchall()
import datetime

today = datetime.date.today()
first = today.replace(day=1)
last_month = first - datetime.timedelta(days=1)
for result in rv:

    reqUrl = "https://api.sednasystem.com/api/getBookingData.asp?api_mode=json&appname=apiboatcharter&token=" + token + "&id_boat=" + str(
        result[2]) + "&date_start=" + last_month.strftime("%Y-%m-%d") + "&date_end=2023-12-31"
    payload_bo = ""
    response_bo = requests.request("GET", reqUrl, data=payload_bo, headers=headersList)
    import datetime as dt

    print(response_bo.text)
    data_json = json.loads(response_bo.text)
    for holiday_bo in data_json['charters']:
        d_dateFrom = int(dt.datetime.strptime(holiday_bo['datestart'], "%Y-%m-%d").timestamp())
        d_dateFrom_string = dt.datetime.strptime(holiday_bo['datestart'], "%Y-%m-%d").strftime(
            "%Y-%m-%d")
        # Convert datetime object to date object.

        d_dateTo = int(dt.datetime.strptime(holiday_bo['dateend'], "%Y-%m-%d").timestamp())
        d_dateTo_string = dt.datetime.strptime(holiday_bo['dateend'], "%Y-%m-%d").strftime("%Y-%m-%d")

        db = client.yatchs_crewd
        yatchs_sedna_bookings = db.yatchs_sedna_bookings
        hash_dates = hashlib.md5(str(d_dateFrom_string + d_dateTo_string).encode("utf-8")).hexdigest()
        yatchs_sedna_bookings.update_one({'boat_id': result[2]}, {'$setOnInsert': {'status': holiday_bo['status'], 'datestart': holiday_bo['datestart'], 'dateend': holiday_bo['dateend'], 'hash_dates': hash_dates}},  upsert=True)