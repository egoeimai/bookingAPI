

from flask import Flask, request, render_template, jsonify
import concurrent.futures
import mysql.connector as mysql
from mysql.connector import Error
from flask_cors import CORS
import json
from app.crew_boats_update import crew_update
from app.crew_boats_update import crew_update_other
from app.BareBoats.bareboats_calls import BareBoats
from app.Crewed.crewed_calls import CrewedBoats
from app.bookings.nausys import Nausys
from app.fxyatching.fxyatching_grud import fxyatching
from app.BareBoats.bareboats_sych import BareBoats_sych
from  app.crew_bookings import Crew_bookings
import threading
import asyncio

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
app.config["BUNDLE_ERRORS"] = True

def html_decode(s):
    """
    Returns the ASCII decoded version of the given HTML string. This does
    NOT remove normal HTML tags like <p>.
    """
    htmlCodes = (
            ("'", '&#39;'),
            ('"', '&quot;'),
            ('>', '&gt;'),
            ('<', '&lt;'),
            ('&', '&amp;')
        )
    for code in htmlCodes:
        s = s.replace(code[1], code[0])
    return s


""" BareBoats Sychronize """

@app.route('/sednalogs/',  methods=['GET'])
def sednalogs():
    bare_logs = BareBoats()
    return bare_logs.get_logs()

@app.route('/crewedlogs/',  methods=['GET'])
def crewedlogs():
    bare_logs = BareBoats()
    return bare_logs.get_logs()

@app.route('/bareboats/',  methods=['GET'])
def bareboats():
    action = request.args.get("action", None)
    boatid = request.args.get("boatid", None)
    if action:
        if action == "get_bare_plan" and boatid:
            bare_boat_plan = BareBoats()
            return bare_boat_plan.get_bareboat_plans(boatid)

        if action == "get_bare_boat" and boatid:
            bare_boat = BareBoats()
            return bare_boat.get_bareboat_characteristics_boat(boatid)

        if action == "get_bareboat_amenities" and boatid:
            bare_boat = BareBoats()
            return bare_boat.get_bareboat_amenities_boat(boatid)
        if action == "get_bareboat_images" and boatid:
            bare_boat = BareBoats()
            return bare_boat.get_bareboat_images_boat(boatid)

    else:
        return "Wrong"


""" Bare Plan Boats Import """
@app.route('/get_bare_plan_import/',  methods=['GET'])
def get_bare_plan_import():
    bare_boat_plan = BareBoats_sych()
    return bare_boat_plan.bareboats_sych_plans()

""" Bare Plan Boats Sychronize """
@app.route('/get_bare_plan/',  methods=['GET'])
def get_bare_plan():
    bare_boat_plan = BareBoats()
    return bare_boat_plan.get_bareboat_plans()

""" Bare Boats Amenities """


task_status = {}
@app.route('/getboat_prices_import/',  methods=['GET'])
def getboat_prices_import():
    bare_boat_plan = BareBoats_sych()
    duration = 10
    """Start a background task with the specified duration."""
    executor = concurrent.futures.ThreadPoolExecutor()
    future = executor.submit(bare_boat_plan.baraboats_sych_prices, duration)
    #print(future.result())
    task_status[1] = {"status": "running"}

    return jsonify({"message": "Background task started", "task_id": 1})

@app.route("/status/<int:task_id>")
def get_task_status(task_id):

    """Get the status of the specified background task."""
    if task_id in task_status:
        return jsonify(task_status[task_id])
    else:
        return jsonify({"message": "Task not found"})


@app.route('/getboat_amenities_import/',  methods=['GET'])
def getboat_amenities_import():
    bare_boat_plan = BareBoats_sych()
    duration = 10
    """Start a background task with the specified duration."""
    executor = concurrent.futures.ThreadPoolExecutor()
    future = executor.submit(bare_boat_plan.baraboats_sych_amenities, duration)
    #print(future.result())

    task_status[1] = {"status": "running"}
    return jsonify({"message": "Background task started", "task_id": 1})


@app.route('/getboat_amenities/',  methods=['GET'])
def getboat_amenities():
    bare_boat_plan = BareBoats()
    return bare_boat_plan.get_bareboat_amenities()



@app.route('/getboat_extras_import/',  methods=['GET'])
def getboat_extras_import():
    bare_boat_plan = BareBoats_sych()
    duration = 10
    """Start a background task with the specified duration."""
    executor = concurrent.futures.ThreadPoolExecutor()
    future = executor.submit(bare_boat_plan.bareboats_sych_boat_extras, duration)
    # print(future.result())

    task_status[1] = {"status": "running"}
    return jsonify({"message": "Background task started", "task_id": 1})



@app.route('/getboat_images_import/',  methods=['GET'])
def getboat_images_import():
    bare_boat_plan = BareBoats_sych()
    duration = 10
    """Start a background task with the specified duration."""
    executor = concurrent.futures.ThreadPoolExecutor()
    future = executor.submit(bare_boat_plan.bareboasts_sych_boat_images, duration)
    # print(future.result())

    task_status[1] = {"status": "running"}
    return jsonify({"message": "Background task started", "task_id": 1})


""" Get BareBoat Extras """

@app.route('/getboat_extras/',  methods=['GET'])
def getboats_extras():
    boatid = request.args.get("boatid", None)
    bare_boat_plan = BareBoats()
    return bare_boat_plan.get_bareboat_extras(boatid)


""" BareBoats Amenities Per Boat Sychronize """
@app.route('/getboat_amenities_per_boat/',  methods=['GET'])
def getboat_amenities_per_boat():
    boatid = request.args.get("boatid", None)
    bare_boat_plan = BareBoats()
    return bare_boat_plan.get_bareboat_amenities_boat(boatid)


""" BareBoats characteristics """
@app.route('/getboats/',  methods=['GET'])
def getboats():
    bare_boat= BareBoats()
    return bare_boat.get_bareboat_characteristics()


""" BareBoats characteristics Sychronize Per Boat """
@app.route('/getboat_bare/',  methods=['GET'])
def getboat_bare():
    boatid = request.args.get("boatid", None)
    bare_boat = BareBoats()
    return bare_boat.get_bareboat_characteristics_boat(boatid)


""" Import Crewed Boats Sychronize """
@app.route('/import_crewd_boats/',  methods=['GET'])
def import_crewd_boats():
    crew_boat = CrewedBoats()
    return crew_boat.import_all_crew_boasts()


""" Crew Boats characteristics Sychronize """
@app.route('/get_crewd_boats/',  methods=['GET'])
def get_crewd_boats():
    crew_boat = CrewedBoats()
    return crew_boat.get_all_crew_boasts()

""" Crew Boats import/update bookings Sychronize """
@app.route('/crewed_update_bokkings/',  methods=['GET'])
def crewed_update_bokkings():
    crew_boat = Crew_bookings()
    return crew_boat.crew_update_bookings()

""" Crew Boats import/update bookings Sychronize """
@app.route('/select_free_bookings/',  methods=['GET'])
def select_free_bookings():
    start = request.args.get("startdate", None)
    end = request.args.get("enddate", None)
    crew_boat = Crew_bookings()
    return crew_boat.select_free_bookings(start, end)








""" Crew Boats import/update bookings Sychronize """
@app.route('/crewed_get_bookings/',  methods=['POST'])
def crewed_get_bookings():
    data = request.json
    print(data)
    crew_boat = Crew_bookings()
    return crew_boat.crew_get_bookings(data['boat_id'])


""" Crew Boats characteristics Sychronize By Id """

@app.route('/get_crewd_boat/',  methods=['GET'])
def get_crewd_boat():
    boatid = request.args.get("boatid", None)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boats` LEFT JOIN crew_boats_basic ON crew_boats.boat_id = crew_boats_basic.boat_id LEFT JOIN crew_images_boats ON crew_images_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_boat_crewd on crew_boat_crewd.boat_id = crew_boats.boat_id LEFT JOIN crew_video_boats ON crew_video_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_amenties ON crew_amenties.boat_id = crew_boats.boat_id LEFT JOIN crew_characteristics ON crew_characteristics.boat_id = crew_boats.boat_id LEFT JOIN crew_water_sports ON crew_water_sports.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtothertoys ON crew_yachtothertoys.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtotherentertain ON crew_yachtotherentertain.boat_id = crew_boats.boat_id LEFT JOIN crewed_areas ON crewed_areas.boat_id = crew_boats.boat_id WHERE  crew_boats.boat_id = "' + str(boatid) + '";')

            rv = cursor.fetchall()
            json_data = []

            for result in rv:
                print(result)
                content = {"name": result[1], "id": result[3], "bt_type": result[2], "widthboat": result[6],
                           "widthboatft": result[7], "cabins": result[10], "nbper": result[9], "buildyear": result[8],
                           "builder": result[14], "crew": result[11], "lowprice": result[12], "highprice": result[13],
                           "mainimage": result[24], "extraimages": result[25], "port": result[15],
                           "num_crew": result[30], "captainname": result[31], "captainnation": result[32],
                           "captainborn": result[33], "captainlang": result[34], "crewname": result[35],
                           "crewtitle": result[36], "crewnation": result[37], "crewborn": result[38],
                           "crewtext": result[39], "image1": result[40], "image2": result[41], "image3": result[42], "image4": result[43], "image5": result[44], "image6": result[45], "image7": result[46], "image8": result[47], "image9": result[48], "image10": result[49], "video_url": result[55],
                           "description": result[16], "price_details": result[17], "locations_details": result[18],
                           "broker_notes": result[19], "yachtRefit": result[20], "yachtOtherPickup": result[152], "yachtSummerArea": result[153], "yachtPrefPickup": result[152]}
                json_data.append(content)
        return jsonify(json_data)

    except Error as e:
        return (e)


""" Crew Boats Amenties Sychronize """

@app.route('/get_crewd_amenties_perboat/',  methods=['GET'])
def get_crewd_amenties_perboat():
    boatid = request.args.get("boatid", None)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_amenties` LEFT JOIN crew_characteristics ON crew_characteristics.boat_id = crew_amenties.boat_id LEFT JOIN crew_yachtotherentertain ON crew_yachtotherentertain.boat_id = crew_amenties.boat_id WHERE  crew_amenties.boat_id = "' + str(boatid) + '";')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "stero": result[2], "sattv": result[3], "ipod": result[4], "sunawing": result[5], "hammocock": result[6], "windscoops": result[7], "deckshower": result[8], "bimini": result[9], "specialdiets": result[10], "kosher": result[11], "bbq": result[12], "numdinein":result[13], "nudechart":result[14], "hairdryer":result[15], "hatch":result[16], "crewsmoke":result[17], "guestsmoke":result[18], "guestpet":result[19], "childerallow":result[20], "gym":result[21], "elevator":result[22], "wheelchairaccess":result[23], "genarator":result[24], "inventer":result[25], "icemaker":result[27], "stabilizer":result[28], "internet":result[29], "greenwater":result[30], "greenreusebottle":result[31], "showers":result[36], "tubs":result[37], "washbasins":result[38], "heads":result[39], "electricheads":result[40], "helipad":result[41], "jacuzzi":result[42], "ac":result[43], "prefpickup":result[44], "otherpickup":result[45], "engines":result[46], "fuel":result[47], "speed":result[48], "maxspeed":result[49], "accommodations":result[50], "other":result[55]}
                json_data.append(content)

        return jsonify(json_data)

    except Error as e:
        return (e)

""" Crew Boats WaterSports Sychronize """
@app.route('/get_crewd_watersports_perboat/',  methods=['GET'])
def get_crewd_watersports_perboat():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_water_sports` LEFT JOIN `crew_yachtothertoys` ON `crew_yachtothertoys`.`boat_id` = `crew_water_sports`.`boat_id`  WHERE  `crew_water_sports`.`boat_id`= "' + str(boatid) + '" ORDER BY `crew_water_sports`.`id` DESC;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "dinghy": result[2], "dinghyhp": result[3], "dinghypax": result[4], "adultsskies": result[5], "kidskis": result[6], "jetskies": result[7], "waverun": result[8], "kneeboard": result[9], "paddle": result[10], "windsurf": result[11], "gearsnorkel": result[12], "tubes":result[13], "scurfer":result[14], "wakeboard":result[15], "mankayak":result[16], "mankayak2":result[17], "seabob":result[18], "seascooter":result[19], "kiteboarding":result[20], "fishinggear":result[21], "fishinggeartype":result[22], "fishinggearnum":result[23], "deepseafish":result[24], "underwatercam":result[25], "watervideo":result[26], "other":result[31]}
                json_data.append(content)

        return jsonify(json_data)

    except Error as e:
        return (e)




""" Crew Boats Crew Sychronize """


@app.route('/get_crewd_boats_crew/', methods=['GET'])
def get_crewd_boats_crew():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boat_crewd`')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "num_crew": result[2], "captainname": result[3], "captainnation": result[4],
                           "captainborn": result[5], "captainlang": result[6], "crewname": result[7],
                           "crewtitle": result[8], "crewnation": result[9], "crewborn": result[10],
                           "crewtext": result[11], "image1": result[12], "image2": result[13]}
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)


@app.route('/get_crewd_boats_layout/', methods=['GET'])
def get_crewd_boats_layout():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crewd_plan`  WHERE `boat_id`= "' + str(boatid) + '";')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "layout": result[2]}
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)


@app.route('/get_crewd_boats_log/', methods=['GET'])
def get_crewd_boats_log():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boats_update_log` ORDER BY `crew_boats_update_log`.`id` DESC LIMIT 1;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"created": result[2], "log": result[1]}
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)







""" Crew Boats Videos Sychronize """

@app.route('/get_crewd_videos/',  methods=['GET'])
def get_crewd_videos():
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_video_boats` WHERE `video_url` is NOT NULL;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "video_url": result[2]}
                json_data.append(content)

            return jsonify( json_data)

    except Error as e:
        return (e)


""" Crew Boats Reviews Sychronize """

@app.route('/get_crewd_reviews/',  methods=['GET'])
def get_crewd_reviews():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boats_reviews` WHERE `boat_id`= "' + str(boatid) + '";')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"review1": result[2], "review2": result[3], "review3": result[4]}
                json_data.append(content)

            return jsonify( json_data)

    except Error as e:
        return (e)


""" Crew Boats Menu Sychronize """

@app.route('/get_crewd_menu/',  methods=['GET'])
def get_crewd_menu():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_sample_menu`  WHERE `boat_id`= "' + str(boatid) + '";')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                if(result[2]):

                    content = {"boat_id": result[1], "menu": html_decode(result[2]), "image1": result[3], "image2": result[4], "image3": result[5], "image4": result[6], "image5": result[7], "image6": result[8], "image7": result[9], "image8": result[10], "image9": result[11], "image10": result[12]}
                    json_data.append(content)
                else:
                    content = {"boat_id": result[1], "menu": ""}
                    json_data.append(content)


            return jsonify( json_data)

    except Error as e:
        return (e)

""" Crew Boats Amenties Sychronize """
@app.route('/get_crewd_amenties/',  methods=['GET'])
def get_crewd_amenties():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_amenties` LEFT JOIN crew_characteristics ON crew_characteristics.boat_id = crew_amenties.boat_id LEFT JOIN crew_yachtotherentertain ON crew_yachtotherentertain.boat_id = crew_amenties.boat_id;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "stero": result[2], "sattv": result[3], "ipod": result[4], "sunawing": result[5], "hammocock": result[6], "windscoops": result[7], "deckshower": result[8], "bimini": result[9], "specialdiets": result[10], "kosher": result[11], "bbq": result[12], "numdinein":result[13], "nudechart":result[14], "hairdryer":result[15], "hatch":result[16], "crewsmoke":result[17], "guestsmoke":result[18], "guestpet":result[19], "childerallow":result[20], "gym":result[21], "elevator":result[22], "wheelchairaccess":result[23], "genarator":result[24], "inventer":result[25], "icemaker":result[27], "stabilizer":result[28], "internet":result[29], "greenwater":result[30], "greenreusebottle":result[31], "showers":result[34], "tubs":result[35], "washbasins":result[36], "heads":result[37], "electricheads":result[38], "helipad":result[39], "jacuzzi":result[40], "ac":result[41], "prefpickup":result[42], "otherpickup":result[43], "engines":result[44], "fuel":result[45], "speed":result[46], "maxspeed":result[47], "accommodations":result[48], "other":result[51]}
                json_data.append(content)

            return jsonify( json_data)

    except Error as e:
        return (e)



""" Crew Boats Watersports Sychronize """

@app.route('/get_crewd_watersports/',  methods=['GET'])
def get_crewd_watersports():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_water_sports` LEFT JOIN `crew_yachtothertoys` ON `crew_yachtothertoys`.`boat_id` = `crew_water_sports`.`boat_id`;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "dinghy": result[2], "dinghyhp": result[3], "dinghypax": result[4], "adultsskies": result[5], "kidskis": result[6], "jetskies": result[7], "waverun": result[8], "kneeboard": result[9], "paddle": result[10], "windsurf": result[11], "gearsnorkel": result[12], "tubes":result[13], "scurfer":result[14], "wakeboard":result[15], "mankayak":result[16], "mankayak2":result[17], "seabob":result[18], "seascooter":result[19], "kiteboarding":result[20], "fishinggear":result[21], "fishinggeartype":result[22], "fishinggearnum":result[23], "deepseafish":result[24], "underwatercam":result[25], "watervideo":result[26], "other":result[29]}
                json_data.append(content)

            return jsonify( json_data)

    except Error as e:
        return (e)

""" Bare Boats Destinations Sychronize """

@app.route('/getboats_destinations/',  methods=['GET'])
def getboats_destinations():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM boats LEFT JOIN boats_bases on boats_bases.boat_id = boats.boat_id;')
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"name": result[1], "id": result[2], "destination_name": result[6], "id_tbf1": result[7]}
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)


""" Bare Boats Prices Sychronize """

@app.route('/getboat_price/',  methods=['GET'])
def getboat_price():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `boat_prices` WHERE `datestart` >= "2022-06-18" AND `boat_id` = ' + boatid + ' ORDER BY `boat_prices`.`datestart` ASC')
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"datestart": result[2], "dateend": result[3], "price": result[4], "unit": result[5]}
                json_data.append(content)


            return jsonify(json_data)

    except Error as e:
            return (e)









""" Send Sedna To Nausis By Id Boat """





@app.route('/getboat_events/',  methods=['GET'])
def getboat_events():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM boats_booking WHERE boat_id='+boatid+' AND status=0' )
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"start": result[3], "end": result[4]}
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)

@app.route('/sendbooking/',  methods=['GET'])
def sendbooking():
    args = request.args
    reqUrl = "https://api.sednasystem.com/API/insert_charter.asp"

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)"
    }

    payload = ""
    import requests
    response = requests.request("GET", reqUrl, params=args, data=payload, headers=headersList)
    import xml.etree.ElementTree as ET

    json_data = []
    xml = ET.fromstring(response.text)
    print(xml[0].text)

    content = {"cliendid": xml.attrib['status'], "messahe": xml[0].attrib['message']}
    json_data.append(content)

    return jsonify(json_data)


@app.route('/sendclient/',  methods=['GET'])
def sendclient():
    name = request.args.get("name", None)
    email = request.args.get("email", None)
    country = request.args.get("country", None)
    tel = request.args.get("tel", None)
    reqUrl = "https://api.sednasystem.com/api/insertclient.asp?name=" + name  + "&email=" + email + "&country=" + country + "&tel=" + tel + "&choix=ope&refope=ysy171"

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)"
    }

    payload = ""
    import requests
    response = requests.request("GET", reqUrl, data=payload, headers=headersList)
    import xml.etree.ElementTree as ET

    json_data = []
    xml = ET.fromstring(response.text)
    print(xml[0].text)

    content = {"cliendid": xml.attrib['id'], "username": xml[0].text, "password": xml[1].text}
    json_data.append(content)

    return jsonify(json_data)




@app.route('/token')
def gettoken():
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

    return xml[0].attrib['authtoken']




@app.route('/api_react/',  methods=['GET'])
def api_react():
    boatid = request.args.get("boatid", None)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM boats_booking WHERE boat_id='+boatid+' AND status=0 ORDER BY `boats_booking`.`datestart` ASC' )
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            sedna = cursor.fetchall()
            cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN mmk_booking ON mmk_booking.boat_id = boats_apis_sych.mmk_id WHERE boats_apis_sych.sedna_id = ' +boatid+ ' AND mmk_booking.status = 1 ORDER BY `mmk_booking`.`dateFrom` ASC')
            mmk = cursor.fetchall()
            print(mmk)

            cursor.execute(
                'SELECT * FROM `boats_apis_sych` LEFT JOIN nausys_boats_bookings ON nausys_boats_bookings.boat_id = boats_apis_sych.nausys WHERE boats_apis_sych.sedna_id = ' + boatid + ' ORDER BY `nausys_boats_bookings`.`periodFrom` ASC')
            nausys = cursor.fetchall()
            json_data = []
            for result in sedna:
                content = {"sedna_booking_id": result[0], "start": result[3], "end": result[4]}
                json_data.append(content)

            json_data_mmk = []
            for result_mmk in mmk:
                content_mmk = {"start": result_mmk[9], "end": result_mmk[10]}
                json_data_mmk.append(content_mmk)
            json_data_nausys = []
            for result_nausys in nausys:
                content_nausys = {"start": result_nausys[9], "end": result_nausys[10], "status": result_nausys[8]}
                json_data_nausys.append(content_nausys)


            cursor.execute('SELECT * FROM boats LEFT JOIN boat_characteristics on boat_characteristics.boat_id = boats.boat_id LEFT JOIN boats_bases on boats_bases.boat_id = boats.boat_id WHERE boats.boat_id='+boatid)

            rv_data = cursor.fetchall()
            json_data_rv = []
            for result in rv_data:
                content_rv = {"name": result[1], "id": result[2], "bt_type": result[5], "model": result[7],
                           "widthboat": result[8], "nbdoucabin": result[9], "nbsimcabin": result[10],
                           "nbper": result[11], "nbbathroom": result[12], "buildyear": result[13],
                           "std_model": result[14], "builder": result[15], "widthboat_feet": result[16],
                           "bt_comment": result[17], "port": result[21], "port_id": result[22]}
                json_data_rv.append(content_rv)
            data = {'sedna': json_data, 'mmk': json_data_mmk, 'nausys': json_data_nausys, 'data': json_data_rv}
            print(data)
            return jsonify(data)


    except Error as e:
        return (e)











@app.route('/nausys_import_boats/',  methods=['GET'])
def nausys_import_boats():

    boats_bookings =Nausys()
    boats = json.loads(boats_bookings.nausys_import_boats())
    return jsonify(boats)








@app.route('/login/',  methods=['POST'])

def login():
    username = request.args.get("email", None)
    password = request.args.get("password", None)
    import requests
    from uuid import uuid4
    import json
    rand_token = uuid4()
    refreshToken = uuid4()
    print(username)
    if username == "info@fyly.gr" and password == "restFyly761" :
        data = {'token': rand_token, 'refreshToken': refreshToken}
        return jsonify(data)
    else :
        data = {'token': rand_token, 'refreshToken': refreshToken}
        return jsonify(data)









@app.route('/crew_boats_update/',  methods=['GET'])

def crew_boats_update():
    test = crew_update();
    return test




@app.route('/crew_boats_update_other/',  methods=['GET'])

def crew_boats_update_other():
    test = crew_update_other();
    return test

@app.route('/fxyatching_get/',  methods=['GET'])
def fxyatching_get():
    yatch = fxyatching()
    response = yatch.get_yatchs()

    return response

@app.route('/fxyatching_create/',  methods=['GET'])
def fxyatching_create():
    boatid = request.args.get("boatid", None)
    name = request.args.get("name", None)
    yatch = fxyatching()
    response = yatch.create_yatchs(name, boatid)

    return response



""" Crew Boats Watersports Sychronize """

@app.route('/fxyatching_get_all_others/',  methods=['GET'])
def fxyatching_get_all_others():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boats_select` WHERE `is_fyly` = 0;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "name": result[2], "is_import" : result[5]}
                json_data.append(content)

            return jsonify( json_data)

    except Error as e:
        return (e)


@app.route('/fxyatching_import_boats_others/',  methods=['GET'])
def fxyatching_import_boats_others():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boats_select` WHERE `is_fyly` = 0 AND `fx_import` = 0 LIMIT 60')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "name": result[2], "is_import" : result[5]}
                json_data.append(content)
                yatch = fxyatching()
                response = yatch.create_yatchs(result[2], str(result[1]))
                print(response)


                # some JSON:
                test = "UPDATE  `crew_boats_select` SET `fx_import` = " + str(response) + " WHERE `crew_boats_select`.`crew_id` = " + str(result[1])
                cursor.execute("UPDATE  `crew_boats_select` SET `fx_import` = " + str(response) + " WHERE `crew_boats_select`.`crew_id` = " + str(result[1]))
                conn.commit()
                json_data.append(test)
        return jsonify(json_data)

    except Error as e:
        return (e)


@app.route('/fxyatching_import_synch/',  methods=['GET'])
def fxyatching_import_synch():
    yatch = fxyatching()
    return yatch.create_yatchs_import()

@app.route('/fxyatching_import_synch_trigger/',  methods=['GET'])
def fxyatching_import_synch_trigger():
    yatch = fxyatching()
    return yatch.step_yatchs_import()


@app.route('/fx_get_new_boats/',  methods=['GET'])
def fx_get_new_boats():
    import requests
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            mycursor = conn.cursor()
            reqUrl = "http://www.centralyachtagent.com/snapins/snyachts-xml.php?user=1318&apicode=1318FYLY7hSs%d49hjQ"


            import xml.etree.ElementTree as ET
            try:
                parser = ET.XMLParser(encoding="utf-8")
                payload = ""
                response = requests.request("GET", reqUrl, data=payload)
                xml = ET.fromstring(response.text, parser=parser)


                for holiday in xml.findall('yacht'):
                    print(holiday[0].text)
                    sql = "INSERT INTO `crew_fresh` (`crew_fresh_boat_id`)VALUES ('" + holiday[0].text + "')"
                    print(holiday)
                    val = (str(holiday[0].text))
                    mycursor.execute(sql)

                    conn.commit();

            except Error as e:
                print(e)

            return "Resr"
    except Error as e:
        print(e)


@app.route('/check_new_delete/',  methods=['GET'])
def check_new_delete():
    import requests
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        mycursor = conn.cursor()
        if conn.is_connected():
            mycursor.execute('SELECT * FROM crew_boats_select WHERE is_fyly = 0 AND `diagrafei` = "0"')
            rv = mycursor.fetchall()
            Boat_log = ""
            for result in rv:
                print( str(result[1]))
                mycursor.execute("DELETE FROM crew_boats_select  WHERE `crew_id` = " + str(result[1]))
                mycursor.execute("DELETE FROM crew_boats  WHERE `boat_id` = " + str(result[1]))
                mycursor.execute("DELETE FROM crew_boats_reviews  WHERE `boat_id` = " + str(result[1]))
                mycursor.execute("DELETE FROM crew_boat_crewd  WHERE `boat_id` = " + str(result[1]))
                mycursor.execute("DELETE FROM crew_characteristics  WHERE `boat_id` = " + str(result[1]))
                mycursor.execute("DELETE FROM crew_sample_menu  WHERE `boat_id` = " + str(result[1]))
                mycursor.execute("DELETE FROM crew_video_boats  WHERE `boat_id` = " + str(result[1]))
                mycursor.execute("DELETE FROM crew_water_sports  WHERE `boat_id` = " + str(result[1]))
                mycursor.execute("DELETE FROM crew_yachtotherentertain  WHERE `boat_id` = " + str(result[1]))
                mycursor.execute("DELETE FROM crew_yachtothertoys  WHERE `boat_id` = " + str(result[1]))

                conn.commit()


            return "Resr"
    except Error as e:
        print(e)


@app.route('/update_all_boats/',  methods=['GET'])
def update_all_boats():
    yatch = fxyatching()
    response = yatch.get_yatchs_fylys()
    response = yatch.update_yatchs_fylys()

    return response


@app.route('/update_all_boats_bulk/',  methods=['GET'])
def update_all_boats_bulk():
    boatids = request.args.get("boatids", None)
    action = request.args.get("action", None)
    website = request.args.get("website", None)
    yatch = fxyatching()
    print(action)
    #response = yatch.get_yatchs_fylys()
    response = yatch.update_yatchs_fylys_bulk(boatids, action, website)

    return response


@app.route('/update_all_others_bulk/',  methods=['GET'])
def update_all_others_bulk():
    action = request.args.get("action", None)
    website = request.args.get("website", None)
    yatch = fxyatching()
    print(action)
    #response = yatch.get_yatchs_fylys()
    response = yatch.update_yatchs_others_bulk(action, website)

    return response


@app.route('/update_all_others_trigger/',  methods=['GET'])
def update_all_others_trigger():
    action = request.args.get("action", None)
    website = request.args.get("website", None)
    yatch = fxyatching()
    response = yatch.step_yatchs_other(action, website)


    return response






@app.route('/update_all_boats_trigger/',  methods=['GET'])
def update_all_boats_trigger():
    action = request.args.get("action", None)
    website = request.args.get("website", None)
    yatch = fxyatching()
    response = yatch.step_yatchs_import_fyly(action, website)


    return response

@app.route('/fxyatching_get_all_my_boats/',  methods=['GET'])
def fxyatching_get_all_my_boats():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boats_select` WHERE `is_fyly` = 1;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "name": result[2], "is_import" : result[5]}
                json_data.append(content)

            return jsonify( json_data)

    except Error as e:
        return (e)

@app.route('/import_boat/',  methods=['GET'])
def import_boat():
    boatid = request.args.get("boat_id", None)
    name = request.args.get("title", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            sql = 'INSERT INTO `crew_boats_select` (`crew_id`, `crew_name`, `is_fyly`) VALUES (%s, %s, %s);'
            val = (boatid, name, 1)
            cursor.execute(sql, val)
            conn.commit();

    except:
        pass

    return "success"

@app.route('/remove_boat/',  methods=['GET'])
def remove_boat():
    boatid = request.args.get("boat_id", None)
    name = request.args.get("title", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            sql = 'DELETE FROM `crew_boats_select` WHERE `crew_id` = ' + boatid

            cursor.execute(sql)
            conn.commit();

    except:
        pass

    return "success"


@app.route('/search_boat_by_slug/', methods=['GET'])
def search_boat_by_slug():
    slug = request.args.get("term", None)
    import requests
    url = "https://fxyachting.com/graphql/"
    body = """ query NewQuery($slug: String!) {
  fleetBy(slug: $slug) {
    title
          content
          slug
          nonBrandingExtraFields {
            planImage
            mainImageNonBranding
            extraImagesNonBranding {
              extraImageNonBrand
            }
            reviewImagesNonBranding {
              reviewImageNonBranding
            }
          }
          featuredImage {
            node {
              sourceUrl
            }
          }
          boats_fields {
            mainCharacteristics {
              length
              guests
              cabins
              crew
              brand
              built
              cruisingSpeed
              fuelConsumption
              port
            }
            video
            sednaId
            priceFilter
            amenities
            watersports
            priceInfo
            accomodationEquipment
            yachtprefpickup
            yachtsummerarea
            yachtotherpickup
            images {
              exteriorImage {
                id
                sourceUrl
              }
            }
            boatPlan {
              sourceUrl
            }
            menuForBoat
            crewInfo
            reviewsImages {
              reviewImage {
                sourceUrl
              }
            }
          }
          seo {
            metaDesc
            metaKeywords
          }
  }
} 
    """
    variables = {"slug": slug}
    import json
    response = requests.post(url=url, json={"query": body, "variables": variables})
    print("response status code: ", response.status_code)
    if response.status_code == 200:
        print(response.content)
        return json.loads(response.content)


@app.route('/search_boat_by_name/', methods=['GET'])
def search_boat_by_name():
    searchQuery = request.args.get("term", None)
    accesstoken = request.args.get("accesstoken", None)

    import hashlib
    result_accesstoken = hashlib.md5(str("zoneoage").encode("utf-8")).hexdigest()
    print(result_accesstoken)

    import requests
    if accesstoken == result_accesstoken:
        url = "https://fxyachting.com/graphql/"
        body = """     query GetBoats($searchQuery: String) {
          fleets(first: 1000, where: {search: $searchQuery}) {
            edges {
              node {
                id
                slug
                featuredImage {
                  node {
                    sourceUrl
                  }
                }
                title
                boats_fields {
                  priceFilter
                  yachtprefpickup
                  yachtsummerarea
                  yachtotherpickup
                  mainCharacteristics {
                    length
                    guests
                    cabins
                    port
                  }
                }
                nonBrandingExtraFields {
                  mainImageNonBranding
                  extraImagesNonBranding {
                    extraImageNonBrand
                  }
                  reviewImagesNonBranding {
                    reviewImageNonBranding
                  }
                }
              }
            }
          }
        }"""
        variables = {"searchQuery": searchQuery}
        import json
        response = requests.post(url=url, json={"query": body, "variables": variables})
        print("response status code: ", response.status_code)
        if response.status_code == 200:
            print(response.content)
            return json.loads(response.content)
    else :
        json_data = []
        content = {"error": "no valid token"}
        json_data.append(content)

    return jsonify(json_data)



@app.route('/search_boat_by_id/', methods=['GET'])
def search_boat_by_id():
    slug = request.args.get("term", None)
    import requests
    url = "https://fxyachting.com/graphql/"
    body = """ query NewQuery($id: Int!) {
  fleetBy(id: $id) {
    title
          content
          slug
          nonBrandingExtraFields {
            planImage
            mainImageNonBranding
            extraImagesNonBranding {
              extraImageNonBrand
            }
            reviewImagesNonBranding {
              reviewImageNonBranding
            }
          }
          featuredImage {
            node {
              sourceUrl
            }
          }
          boats_fields {
            mainCharacteristics {
              length
              guests
              cabins
              crew
              brand
              built
              cruisingSpeed
              fuelConsumption
              port
            }
            video
            sednaId
            priceFilter
            amenities
            watersports
            priceInfo
            accomodationEquipment
            yachtprefpickup
            yachtsummerarea
            yachtotherpickup
            images {
              exteriorImage {
                id
                sourceUrl
              }
            }
            boatPlan {
              sourceUrl
            }
            menuForBoat
            crewInfo
            reviewsImages {
              reviewImage {
                sourceUrl
              }
            }
          }
          seo {
            metaDesc
            metaKeywords
          }
  }
} 
    """
    variables = {"slug": slug}
    import json
    response = requests.post(url=url, json={"query": body, "variables": variables})
    print("response status code: ", response.status_code)
    if response.status_code == 200:
        print(response.content)
        return json.loads(response.content)

@app.route('/get_fx_boats')
def get_fx_boats():
    import json
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()

            cursor.execute('SELECT * FROM crew_boats_select')
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                json_data.append(dict(zip(row_headers, result)))
            return jsonify(json_data)

    except Error as e:
        return (e)


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == "__main__":
    app.run()
