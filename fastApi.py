from fastapi import FastAPI, BackgroundTasks, Request
import mysql.connector as mysql
from mysql.connector import Error
from pymongo import MongoClient
from bson import BSON
from bson import json_util
import hashlib
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8100",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pymongo.mongo_client import MongoClient
import requests
from pymongo.server_api import ServerApi

uri = "mongodb+srv://nikos:dNf4rEqjMcFcG98r@predifine.vfor3my.mongodb.net/?retryWrites=true&w=majority&connectTimeoutMS=60000"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


class ResponseBody(BaseModel):
    _id: str


@app.post("/start_task/")
async def start_task(background_tasks: BackgroundTasks):
    # Do some processing here
    # ...

    # Schedule a task to run in the background
    background_tasks.add_task(baraboats_sych_prices)

    return {"message": "Task started successfully."}


@app.post("/import_booking_crewed/")
async def start_task(background_tasks: BackgroundTasks):
    # Do some processing here
    # ...

    # Schedule a task to run in the background
    background_tasks.add_task(crewboats_sych_booking)

    return {"message": "Task started successfully."}


def baraboats_sych_prices():
    token = ""
    print(f"Starting background task with duration...")
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            cursor.execute('TRUNCATE TABLE boat_prices;')
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
    response = requests.request("GET", reqUrl, data=payload, headers=headersList)
    import xml.etree.ElementTree as ET
    xml = ET.fromstring(response.text)
    try:
        for boat in xml.findall('boat'):

            prices = boat.findall('prices')
            for price in prices:
                price_inner = price.findall('price')
                for price_val in price_inner:
                    print(price_val.attrib['amount'])
                    sqls_price = "INSERT INTO `boat_prices` (`boat_id`, `datestart`, `dateend`, `amount`, `unitamount`) VALUES (%s, %s, %s, %s, %s);"
                    price_vals = (boat.attrib['id_boat'], price_val.attrib['datestart'], price_val.attrib['dateend'],
                                  price_val.attrib['amount'], price_val.attrib['unitamount'])
                    mycursor.execute(sqls_price, price_vals)
                    conn.commit()

        send_success_email("Update Import Prices", "The prices of BareBoats has been updated")
        print("Background task completed.")
    except:
        send_success_email("Update Import Prices Faild", "The prices of BareBoats has been Faild")


def send_success_email(subject_t, text):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from string import Template

    # check new data type

    username = "development@zonepage.gr"
    password = "Vac51132"
    mail_from = "development@zonepage.gr"
    mail_subject = subject_t
    mail_body = text
    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = "nziozas@gmail.com"
    mimemsg['Subject'] = mail_subject
    mimemsg.attach(MIMEText(mail_body, 'plain'))
    connection = smtplib.SMTP(host='smtp.office365.com', port=587)
    connection.starttls()
    connection.login(username, password)
    connection.send_message(mimemsg)
    connection.quit()


@app.post("/get_bareboat_plans/")
async def get_bareboat_plans():
    try:
        client = MongoClient(
            "mongodb+srv://yachting_solutions:NCJ7mtjQLjqf9ez1@crewed.631yzli.mongodb.net/?retryWrites=true&w=majority")

        print("Connected successfully!!!")
    except:
        print("Could not connect to MongoDB")
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `bare_boat_plans` WHERE `plan_url` is NOT NULL;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "plan_url": result[2]}
                json_data.append(content)
            json_compatible_item_data = jsonable_encoder(json_data)
            db = client.yatchs_crewd
            yatchs_sedna_bookings = db.yatch_plan
            for boat in json_compatible_item_data:
                yatchs_sedna_bookings.insert_one(boat)
            return JSONResponse(content=json_compatible_item_data)



    except Error as e:
        return (e)


@app.post("/update_boats_extra/")
async def update_boats_extra(request: Request):
    student = await request.json()

    for result in student:
        filter_query = {'crew_id': int(result['crew_id'])}
        print(int(result['financial']['apa']))
        update_query = {"$set": {'apa': int(result['financial']['apa']), 'vat': int(result['financial']['vat'])}}
        result = db.crew_boats_apa.update_one(filter_query, update_query)
        print(f"Matched {result.matched_count} documents and updated {result.modified_count} documents")


@app.post("/import_boats/")
async def import_boats():
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi
    uri = "mongodb+srv://nikos:dNf4rEqjMcFcG98r@predifine.vfor3my.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM crew_boats_select')
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))

            json_compatible_item_data = jsonable_encoder(json_data)
            db = client.viewyacht
            yatchs_sedna_bookings = db.crew_boats
            for boat in json_compatible_item_data:
                yatchs_sedna_bookings.insert_one(boat)
            return JSONResponse(content=json_compatible_item_data)
    except Error as e:
        return (e)


@app.get("/get_crew_boats_simple/")
async def get_crew_boats_simple():
    db = client.viewyacht
    crew = list(db.crew_boats.aggregate([
        {
            '$match': {
                'is_fyly': 1
            }
        }, {
            '$lookup': {
                'from': 'crew_boats_details',
                'localField': 'crew_id',
                'foreignField': 'yachtId',
                'as': 'details'
            }
        }, {
            '$unwind': {
                'path': '$details'
            }
        }, {
            '$lookup': {
                'from': 'crew_boats_apa',
                'localField': 'crew_id',
                'foreignField': 'crew_id',
                'as': 'financial'
            }
        }, {
            '$unwind': {
                'path': '$financial'
            }
        }, {
            '$project': {
                '_id': 0,
                'crew_id': 1,
                'crew_name': 1,
                'details': {
                    'yachtPic1': 1
                },
                'financial': {
                    'vat': 1,
                    'apa': 1
                }
            }
        }
    ]))

    print(type(crew))
    json_compatible_item_data = jsonable_encoder(crew)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/get_crew_boats/")
async def get_crew_boats():
    db = client.viewyacht
    crew = list(db.crew_boats.aggregate([
        {
            '$match': {
                'is_fyly': 1

            }
        }, {
            '$lookup': {
                'from': 'crew_boats_details',
                'localField': 'crew_id',
                'foreignField': 'yachtId',
                'as': 'details'
            }
        }, {
            '$unwind': {
                'path': '$details'
            }
        },
        {
            '$lookup': {
                'from': 'crew_boats_apa',
                'localField': 'crew_id',
                'foreignField': 'crew_id',
                'as': 'financial'
            }
        }, {
            '$unwind': {
                'path': '$financial'
            }
        },
        {
            '$project': {
                '_id': 0,
                'crew_id': 1,
                'crew_name': 1,
                'details': {
                    'sizeFeet': 1,
                    'sizeMeter': 1,
                    'yachtPax': 1,
                    'yachtCabins': 1,
                    'yachtYearBuilt': 1,
                    'yachtCrew': 1,
                    'yachtLowNumericPrice': 1,
                    'yachtHighNumericPrice': 1,

                    'yachtAccommodations': 1,
                    'yachtPic1': 1,
                    'yachtHomePort': 1,
                    'yachtDesc1': 1,
                    'yachtOtherToys': 1

                },
                'financial': {
                    'vat': 1,
                    'apa': 1
                }
            }
        }
    ]))

    print(type(crew))
    json_compatible_item_data = jsonable_encoder(crew)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/get_crew_boats_bookings/")
def get_crew_boats_bookings():
    from datetime import datetime

    db = client.viewyacht
    d_dateFrom_string = datetime.strptime("2024-06-16", "%Y-%m-%d")
    d_dateTo_string = datetime.strptime("2024-06-23", "%Y-%m-%d")
    import datetime
    end_date = d_dateTo_string + datetime.timedelta(days=25)

    crew = list(db.crew_boats.aggregate([
        {
            '$match': {
                'is_fyly': 1
            }
        }, {
            '$lookup': {
                'from': 'crew_boats_bookings',
                'localField': 'crew_id',
                'pipeline': [
                    {
                        '$match': {
                            'yachtStartDateNum': {
                                '$gte': d_dateFrom_string
                            },
                            'yachtEndDateNum': {
                                '$lte': end_date
                            }

                        }
                    }
                ],
                'foreignField': 'yachtBookId',
                'as': 'bookings'
            }
        }, {
            '$lookup': {
                'from': 'crew_boats_details',
                'localField': 'crew_id',
                'foreignField': 'yachtId',
                'as': 'details'
            }
        }, {
            '$unwind': {
                'path': '$details'
            }
        },
        {
            '$lookup': {
                'from': 'crew_boats_apa',
                'localField': 'crew_id',
                'foreignField': 'crew_id',
                'as': 'financial'
            }
        }, {
            '$unwind': {
                'path': '$financial'
            }
        },
        {
            '$project': {
                '_id': 0,
                'crew_id': 1,
                'is_fyly': 1,
                'crew_name': 1,
                'bookings': {
                    'yachtStartDateNum': 1,
                    'yachtEndDateNum': 1,
                    'yachtBookDesc': 1
                },
                'details': {
                    'sizeFeet': 1,
                    'sizeMeter': 1,
                    'yachtPax': 1,
                    'yachtCabins': 1,
                    'yachtYearBuilt': 1,
                    'yachtCrew': 1,
                    'yachtLowNumericPrice': 1,
                    'yachtHighNumericPrice': 1,
                    'yachtAccommodations': 1,
                    'yachtPic1': 1,
                    'yachtHomePort': 1,
                    'yachtDesc1': 1,
                    'yachtOtherToys': 1
                },
                'financial': {
                    'vat': 1,
                    'apa': 1
                }
            }
        }
    ]))

    print(type(crew))
    json_compatible_item_data = jsonable_encoder(crew)
    return JSONResponse(content=json_compatible_item_data)


@app.post("/import_crew_boats/")
def import_crew_boats():
    from pymongo.mongo_client import MongoClient
    import requests
    from pymongo.server_api import ServerApi
    uri = "mongodb+srv://nikos:dNf4rEqjMcFcG98r@predifine.vfor3my.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM crew_boats_select')
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            rv = cursor.fetchall()
            json_data = []

            for result in rv:
                reqUrl = "https://www.centralyachtagent.com/snapins/json-ebrochure.php?user=1360&idin=" + str(
                    result[1]) + "&apicode=AY1360ya63$21t"
                payload = ""
                response = requests.request("GET", reqUrl, data=payload)
                jsonResponse = response.json()
                jsonResponse['yacht']['hash'] = hashlib.md5(str(jsonResponse).encode("utf-8")).hexdigest()
                print("Entire JSON response")
                db = client.viewyacht
                yatchs_sedna_bookings = db.crew_boats_details
                yatchs_sedna_bookings.insert_one(jsonResponse['yacht'])

    except Error as e:
        return (e)
    import requests
    reqUrl = "https://www.centralyachtagent.com/snapins/json-ebrochure.php?user=1360&idin=8844&apicode=AY1360ya63$21t"
    payload = ""
    response = requests.request("GET", reqUrl, data=payload)
    jsonResponse = response.json()
    jsonResponse['yacht']['hash'] = hashlib.md5(str(jsonResponse).encode("utf-8")).hexdigest()
    print("Entire JSON response")
    return jsonResponse


@app.post("/crewboats_sych_booking/")
def crewboats_sych_booking():
    token = ""

    from pymongo.mongo_client import MongoClient
    import requests
    from pymongo.server_api import ServerApi

    uri = "mongodb+srv://nikos:dNf4rEqjMcFcG98r@predifine.vfor3my.mongodb.net/?retryWrites=true&w=majority"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)


    except Error as e:
        print(e)

    import requests
    import datetime as dt
    from datetime import datetime

    cursor.execute('SELECT crew_id FROM crew_boats_select WHERE is_fyly = 1')
    row_headers = [x[0] for x in cursor.description]  # this will extract row headers
    rv = cursor.fetchall()
    Boat_log = ""
    for boats in rv:
        reqUrl = "http://www.centralyachtagent.com/snapins/json-calendar.php?idin=" + str(boats[0]) + "&user=1318"
        payload = ""
        response = requests.request("GET", reqUrl, data=payload)
        jsonResponse = response.json()
        print("Entire JSON response")

        print(str(jsonResponse['calendar']) + "  " + str(boats[0]))
        if type(jsonResponse['calendar']) == list:
            booking_dates = jsonResponse['calendar']
            print(booking_dates)

            for booking_date in booking_dates:
                print(booking_date)
                hash_val_booking = (
                booking_date['yachtBookId'], booking_date['yachtStartDateNum'], booking_date['yachtEndDateNum'],
                booking_date['yachtBookDesc'])
                booking_date['hash'] = hashlib.md5(str(hash_val_booking).encode("utf-8")).hexdigest()
                d_dateFrom_string = datetime.strptime(booking_date['yachtStartDateNum'], "%Y-%m-%d")
                d_dateTo_string = datetime.strptime(booking_date['yachtEndDateNum'], "%Y-%m-%d")
                booking_date['yachtBookId'] = int(booking_date['yachtBookId'])

                booking_date['yachtStartDateNum'] = d_dateFrom_string
                booking_date['yachtEndDateNum'] = d_dateTo_string
                db = client.viewyacht
                yatchs_sedna_bookings = db.crew_boats_bookings
                yatchs_sedna_bookings.insert_one(booking_date)

    return "Complete"


@app.post('/add_mail_brochure/')
async def add_mail_brochure(request: Request):
    from datetime import datetime
    student = await request.json()
    student['created_date'] = datetime.now()
    db = client.viewyacht
    yatchs_sedna_bookings = db.crew_boats_pridefine
    yatchs_sedna_bookings.insert_one(student)

    print(student)


@app.get('/get_history/')
async def add_mail_brochure():
    db = client.viewyacht

    history = list(db.crew_boats_pridefine.aggregate(
        [
            {
                '$unset': '_id'

            }
        ]))

    json_compatible_item_data = jsonable_encoder(history)
    return JSONResponse(content=json_compatible_item_data)
