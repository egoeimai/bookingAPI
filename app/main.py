
from flask import Flask, request, render_template, jsonify
import mysql.connector as mysql
from mysql.connector import Error
from flask_cors import CORS
import json
import smtplib, ssl

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



""" Bare Plan Boats Sychronize """
@app.route('/get_bare_plan/',  methods=['GET'])
def get_bare_plan():
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
            json_output = json.dumps(rv)
            return jsonify( json_data)

    except Error as e:
        return (e)

""" Get BareBoat Extras """

@app.route('/getboat_extras/',  methods=['POST'])
def getboats_extras():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM boats_extras WHERE boat_id=' + boatid)
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"id_opt": result[1], "id_opt_bt": result[2], "name": result[3], "price": result[4], "per": result[5]}
                json_data.append(content)


            return jsonify(json_data)

    except Error as e:
            return (e)


""" Bare Boats Amenities Sychronize """

@app.route('/getboat_amenities/',  methods=['GET'])
def getboat_amenities():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM boats')
            boats = cursor.fetchall()
            json_data = []
            for boat in boats:
                content = ""
                cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(boat[2]) + '" and topic = "Layout";')
                rv = cursor.fetchall()

                html = "<ul>"
                for result in rv:
                    html = html + "<li>" + result[3] + " : " + result[4] + "</li>"
                html = html + "</ul>"

                cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' +str(boat[2]) + '" and topic = "Amenities";')
                rv = cursor.fetchall()
                amenities = "<ul>"
                for result in rv:
                    amenities = amenities + "<li>" + result[3] + "</li>"
                amenities = amenities + "</ul>"

                cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' +str(boat[2]) + '" and topic = "Characteristics";')
                rv = cursor.fetchall()
                Characteristics = "<ul>"
                for result in rv:
                    Characteristics = Characteristics + "<li>" + result[3] + " : " + result[4] + " " + result[5] +"</li>"
                Characteristics = Characteristics + "</ul>"

                cursor.execute(
                    'SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' +str(boat[2]) + '" and topic = "Inventory";')
                rv = cursor.fetchall()
                Inventory = "<ul>"
                for result in rv:
                    Inventory = Inventory + "<li>" + result[3] + "</li>"
                Inventory = Inventory + "</ul>"

                cursor.execute(
                    'SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' +str(boat[2]) + '" and topic = "Safety Equipment";')
                rv = cursor.fetchall()
                Safety_Equipment = "<ul>"
                for result in rv:
                    Safety_Equipment = Safety_Equipment + "<li>" + result[3] + "</li>"
                Safety_Equipment = Safety_Equipment + "</ul>"

                cursor.execute('SELECT plan_url FROM `bare_boat_plans` WHERE `boat_id` = "' + str(boat[2]) + '";')
                rv_plan = cursor.fetchall()

                content = {"id":boat[2], "layout": html, "amenities": amenities, "Characteristics": Characteristics, "Inventory":Inventory, "Safety_Equipment": Safety_Equipment, "plans": rv_plan[0]}
                json_data.append(content)





        return jsonify(json_data)

    except Error as e:
        return (e)

""" BareBoats Amenities Per Boat Sychronize """
@app.route('/getboat_amenities_per_boat/',  methods=['GET'])
def getboat_amenities_per_boat():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()

            json_data = []

            content = ""
            cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(boatid) + '" and topic = "Layout";')
            rv = cursor.fetchall()

            html = "<ul>"
            for result in rv:
                html = html + "<li>" + result[3] + " : " + result[4] + "</li>"
            html = html + "</ul>"

            cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' +str(boatid) + '" and topic = "Amenities";')
            rv = cursor.fetchall()
            amenities = "<ul>"
            for result in rv:
                amenities = amenities + "<li>" + result[3] + "</li>"
            amenities = amenities + "</ul>"

            cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' +str(boatid) + '" and topic = "Characteristics";')
            rv = cursor.fetchall()
            Characteristics = "<ul>"
            for result in rv:
                Characteristics = Characteristics + "<li>" + result[3] + " : " + result[4] + " " + result[5] +"</li>"
            Characteristics = Characteristics + "</ul>"

            cursor.execute(
                'SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' +str(boatid) + '" and topic = "Inventory";')
            rv = cursor.fetchall()
            Inventory = "<ul>"
            for result in rv:
                Inventory = Inventory + "<li>" + result[3] + "</li>"
            Inventory = Inventory + "</ul>"

            cursor.execute(
                'SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' +str(boatid) + '" and topic = "Safety Equipment";')
            rv = cursor.fetchall()
            Safety_Equipment = "<ul>"
            for result in rv:
                Safety_Equipment = Safety_Equipment + "<li>" + result[3] + "</li>"
            Safety_Equipment = Safety_Equipment + "</ul>"

            cursor.execute('SELECT plan_url FROM `bare_boat_plans` WHERE `boat_id` = "' + str(boatid) + '";')
            rv_plan = cursor.fetchall()

            content = {"id":boatid, "layout": html, "amenities": amenities, "Characteristics": Characteristics, "Inventory":Inventory, "Safety_Equipment": Safety_Equipment, "plans": rv_plan[0]}
            json_data.append(content)





        return jsonify(json_data)

    except Error as e:
        return (e)


""" BareBoats characteristics Sychronize """
@app.route('/getboats/',  methods=['GET'])
def getboats():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM boats LEFT JOIN boat_characteristics on boat_characteristics.boat_id = boats.boat_id LEFT JOIN boats_bases on boats_bases.boat_id = boats.boat_id WHERE boat_characteristics.crew = "Bare Boat";')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"name": result[1], "id": result[2], "bt_type": result[5], "model": result[7], "widthboat": result[8], "nbdoucabin": result[9], "nbsimcabin": result[10], "nbper": result[11], "nbbathroom": result[12], "buildyear": result[13], "std_model": result[14], "builder": result[15], "widthboat_feet": result[16], "bt_comment": result[17], "port": result[21], "port_id": result[22]}
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)

""" BareBoats characteristics Sychronize """
@app.route('/getboat_bare/',  methods=['GET'])
def getboat_bare():
    boatid = request.args.get("boatid", None)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM boats LEFT JOIN boat_characteristics on boat_characteristics.boat_id = boats.boat_id LEFT JOIN boats_bases on boats_bases.boat_id = boats.boat_id WHERE boat_characteristics.crew = "Bare Boat" AND boats.boat_id = "' + str(boatid) + '";')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"name": result[1], "id": result[2], "bt_type": result[5], "model": result[7], "widthboat": result[8], "nbdoucabin": result[9], "nbsimcabin": result[10], "nbper": result[11], "nbbathroom": result[12], "buildyear": result[13], "std_model": result[14], "builder": result[15], "widthboat_feet": result[16], "bt_comment": result[17], "port": result[21], "port_id": result[22]}
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)

""" Crew Boats characteristics Sychronize """
@app.route('/get_crewd_boats/',  methods=['GET'])
def get_crewd_boats():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boats` LEFT JOIN crew_boats_basic ON crew_boats.boat_id = crew_boats_basic.boat_id LEFT JOIN crew_images_boats ON crew_images_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_boat_crewd on crew_boat_crewd.boat_id = crew_boats.boat_id LEFT JOIN crew_video_boats ON crew_video_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_amenties ON crew_amenties.boat_id = crew_boats.boat_id LEFT JOIN crew_characteristics ON crew_characteristics.boat_id = crew_boats.boat_id LEFT JOIN crew_water_sports ON crew_water_sports.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtothertoys ON crew_yachtothertoys.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtotherentertain ON crew_yachtotherentertain.boat_id = crew_boats.boat_id;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"name": result[1], "id": result[3], "bt_type": result[2], "widthboat": result[6], "widthboatft": result[7], "cabins": result[10], "nbper": result[9], "buildyear": result[8], "builder": result[14], "crew": result[11], "lowprice": result[12], "highprice": result[13], "mainimage":result[23], "extraimages":result[24], "port":result[15], "num_crew": result[27], "captainname": result[28], "captainnation": result[29],
                           "captainborn": result[30], "captainlang": result[31], "crewname": result[32],
                           "crewtitle": result[33], "crewnation": result[34], "crewborn": result[35],
                           "crewtext": result[36], "image1": result[37], "image2": result[38], "video_url": result[41], "description": result[16], "price_details": result[17], "locations_details": result[18], "broker_notes": result[19] }
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)

""" Crew Boats characteristics Sychronize By Id """

@app.route('/get_crewd_boat/',  methods=['GET'])
def get_crewd_boat():
    boatid = request.args.get("boatid", None)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boats` LEFT JOIN crew_boats_basic ON crew_boats.boat_id = crew_boats_basic.boat_id LEFT JOIN crew_images_boats ON crew_images_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_boat_crewd on crew_boat_crewd.boat_id = crew_boats.boat_id LEFT JOIN crew_video_boats ON crew_video_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_amenties ON crew_amenties.boat_id = crew_boats.boat_id LEFT JOIN crew_characteristics ON crew_characteristics.boat_id = crew_boats.boat_id LEFT JOIN crew_water_sports ON crew_water_sports.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtothertoys ON crew_yachtothertoys.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtotherentertain ON crew_yachtotherentertain.boat_id = crew_boats.boat_id WHERE  crew_boats.boat_id = "' + str(boatid) + '";')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"name": result[1], "id": result[3], "bt_type": result[2], "widthboat": result[6],
                           "widthboatft": result[7], "cabins": result[10], "nbper": result[9], "buildyear": result[8],
                           "builder": result[14], "crew": result[11], "lowprice": result[12], "highprice": result[13],
                           "mainimage": result[23], "extraimages": result[24], "port": result[15],
                           "num_crew": result[27], "captainname": result[28], "captainnation": result[29],
                           "captainborn": result[30], "captainlang": result[31], "crewname": result[32],
                           "crewtitle": result[33], "crewnation": result[34], "crewborn": result[35],
                           "crewtext": result[36], "image1": result[37], "image2": result[38], "video_url": result[41],
                           "description": result[16], "price_details": result[17], "locations_details": result[18],
                           "broker_notes": result[19]}
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
                content = {"boat_id": result[1], "stero": result[2], "sattv": result[3], "ipod": result[4], "sunawing": result[5], "hammocock": result[6], "windscoops": result[7], "deckshower": result[8], "bimini": result[9], "specialdiets": result[10], "kosher": result[11], "bbq": result[12], "numdinein":result[13], "nudechart":result[14], "hairdryer":result[15], "hatch":result[16], "crewsmoke":result[17], "guestsmoke":result[18], "guestpet":result[19], "childerallow":result[20], "gym":result[21], "elevator":result[22], "wheelchairaccess":result[23], "genarator":result[24], "inventer":result[25], "icemaker":result[27], "stabilizer":result[28], "internet":result[29], "greenwater":result[30], "greenreusebottle":result[31], "showers":result[34], "tubs":result[35], "washbasins":result[36], "heads":result[37], "electricheads":result[38], "helipad":result[39], "jacuzzi":result[40], "ac":result[41], "prefpickup":result[42], "otherpickup":result[43], "engines":result[44], "fuel":result[45], "speed":result[46], "maxspeed":result[47], "accommodations":result[48], "other":result[51]}
                json_data.append(content)
            json_output = json.dumps(rv)
            return jsonify( json_data)

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
            cursor.execute('SELECT * FROM `crew_water_sports` LEFT JOIN `crew_yachtothertoys` ON `crew_yachtothertoys`.`boat_id` = `crew_water_sports`.`boat_id`  WHERE  `crew_water_sports`.`boat_id`= "' + str(boatid) + '";')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "dinghy": result[2], "dinghyhp": result[3], "dinghypax": result[4], "adultsskies": result[5], "kidskis": result[6], "jetskies": result[7], "waverun": result[8], "kneeboard": result[9], "paddle": result[10], "windsurf": result[11], "gearsnorkel": result[12], "tubes":result[13], "scurfer":result[14], "wakeboard":result[15], "mankayak":result[16], "mankayak2":result[17], "seabob":result[18], "seascooter":result[19], "kiteboarding":result[20], "fishinggear":result[21], "fishinggeartype":result[22], "fishinggearnum":result[23], "deepseafish":result[24], "underwatercam":result[25], "watervideo":result[26], "other":result[29]}
                json_data.append(content)
            json_output = json.dumps(rv)
            return jsonify( json_data)

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
            json_output = json.dumps(rv)
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
            json_output = json.dumps(rv)
            return jsonify( json_data)

    except Error as e:
        return (e)


""" Crew Boats Menu Sychronize """

@app.route('/get_crewd_menu/',  methods=['GET'])
def get_crewd_menu():
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_sample_menu` WHERE `text_menu` is NOT NULL;')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"boat_id": result[1], "menu": html_decode(result[2])}
                json_data.append(content)
            json_output = json.dumps(rv)
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
            json_output = json.dumps(rv)
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
            json_output = json.dumps(rv)
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


""" Sedna To MMK Sychronize """

@app.route('/get_sedna_to_mmk/',  methods=['GET'])
def get_sedna_to_mmk():
    boatid = request.args.get("boatid", None)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly', password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `boats_apis_sych`')
            boats = cursor.fetchall()
            mmk_log = ""
            log_count = 1
            for result_boas in boats:
                cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN mmk_booking ON mmk_booking.boat_id = boats_apis_sych.mmk_id WHERE boats_apis_sych.sedna_id = ' + str(result_boas[1]) + ' AND mmk_booking.status = 1')
                mmk = cursor.fetchall()
                cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN boats_booking ON boats_booking.boat_id = boats_apis_sych.sedna_id WHERE boats_apis_sych.sedna_id = ' + str(result_boas[1]) + ' AND boats_booking.status = 0;')
                sedna = cursor.fetchall()
                import requests
                import json

                if len(mmk) < len(sedna):

                    for result in sedna:
                        exist = 0
                        for i, d in enumerate(mmk):

                            if d[15] == result[10]:
                                exist = 1
                                break
                        else:
                            i = -1
                        if exist == 0:
                            url = "https://www.booking-manager.com/api/v2/reservation"
                            print(result[9].strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
                            payload = json.dumps({
                                "dateFrom": result[8].strftime('%Y-%m-%dT%H:%M:%S'),
                                "dateTo": result[9].strftime('%Y-%m-%dT%H:%M:%S'),
                                "yachtId": result_boas[2],
                                "status": 2
                            })
                            headers = {
                                'Authorization': 'Bearer 837-d6973f84d9b2752274d9695ee411b01176871329d36b12872601a0837b390374104b7fa3542e0aefade6f65835bd09885f372592ddc57b44a2a853602dd03cc2',
                                'Content-Type': 'application/json'
                            }

                            response = requests.request("POST", url, headers=headers, data=payload)

                            print(response.text)
                            print("Σκάφος: " + str(result[3]) + " - Κράτηση:  " + result[8].strftime('%Y-%m-%d') + " - " + result[9].strftime('%Y-%m-%d') + " <br><strong>Σφάλμα</strong>:  " + response.text)
                            mmk_log = mmk_log + "<p>Σκάφος: " +  str(result[3]) + " - Κράτηση:  " + result[8].strftime('%Y-%m-%d') + " - " + result[9].strftime('%Y-%m-%d') + "  <br><strong>Σφάλμα</strong>:  " + response.text + "</p>"
                            log_count = log_count + 1
        print(log_count)
        sql_bases = "INSERT INTO api_mmk_sych (log, log_count) VALUES ('" + mmk_log + "', '" + str(log_count) + "');"
        val_bases = mmk_log
        cursor.execute(sql_bases, val_bases)
        conn.commit()


        return mmk_log

    except Error as e:
        return (e)



""" Sedna To Nausys Sychronize """


@app.route('/get_sedna_to_nausys/',  methods=['GET'])
def get_sedna_to_nausys():
    boatid = request.args.get("boatid", None)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly', password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `boats_apis_sych`')
            boats = cursor.fetchall()
            nausys_log = ""
            log_count = 1
            for result_boats in boats:
                cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN nausys_boats_bookings ON nausys_boats_bookings.boat_id = boats_apis_sych.nausys WHERE boats_apis_sych.sedna_id = ' + str(result_boats[1]) + ' AND nausys_boats_bookings.status = "RESERVATION"')
                nausys = cursor.fetchall()
                cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN boats_booking ON boats_booking.boat_id = boats_apis_sych.sedna_id WHERE boats_apis_sych.sedna_id = ' + str(result_boats[1]) + ' AND boats_booking.status = 0;')
                sedna = cursor.fetchall()
                import requests
                import json

                if len(nausys) < len(sedna):

                    for result in sedna:
                        exist = 0
                        for i, d in enumerate(nausys):

                            if d[12] == result[10]:
                                exist = 1
                                print(d)
                                break
                        else:
                            i = -1







        return nausys_log

    except Error as e:
        return (e)

""" Send Sedna To MMK By Id Boat """

@app.route('/send_sedna_to_mmk_id/',  methods=['GET'])
def send_sedna_to_mmk_id():
    boatid = request.args.get("boatid", None)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `boats_apis_sych` where sedna_id='+boatid)
            boats = cursor.fetchall()
            import requests
            import json
            url = "https://www.booking-manager.com/api/v2/reservation"

            payload = json.dumps({
                "dateFrom": boats[7].strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                "dateTo": boats[8].strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                "yachtId": boats[2],
                "status": 2
            })
            headers = {
                'Authorization': 'Bearer 837-d6973f84d9b2752274d9695ee411b01176871329d36b12872601a0837b390374104b7fa3542e0aefade6f65835bd09885f372592ddc57b44a2a853602dd03cc2',
                'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)


        return response.text

    except Error as e:
        return (e)





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


@app.route('/api_get_boats/',  methods=['GET'])
def api_get_boats():
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM boats LEFT JOIN boat_characteristics on boat_characteristics.boat_id = boats.boat_id LEFT JOIN boats_bases on boats_bases.boat_id = boats.boat_id')
            rv_data = cursor.fetchall()
            json_data_rv = []
            for result in rv_data:
                content_rv = {"name": result[1], "id": result[2]}
                json_data_rv.append(content_rv)
            cursor.execute('SELECT * FROM `api_mmk_sych` ORDER BY sych_id DESC LIMIT 15')
            mmk_log_data = cursor.fetchall()
            json_mmk_log_data = []
            for mmk_result in mmk_log_data:
                mmk_content_rv = {
                    "id": mmk_result[0], "log":mmk_result[1], "date":mmk_result[3], "count":mmk_result[2]
                }
                json_mmk_log_data.append(mmk_content_rv)


            data = {'data': json_data_rv, 'mmk_logs': json_mmk_log_data }
            print(data)
            return jsonify(data)


    except Error as e:
        return (e)

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
                content = {"start": result[3], "end": result[4]}
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


@app.route('/api_react_date/',  methods=['GET'])
def api_react_date():
    boatid = request.args.get("boatid", None)
    month = request.args.get("month", None)
    year = request.args.get("year", None)


    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM boats_booking WHERE boat_id='+boatid+' AND  YEAR(datestart) = '+year+' AND MONTH(datestart) = '+month+'  AND status=0 ORDER BY `boats_booking`.`datestart` ASC' )
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            sedna = cursor.fetchall()

            cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN mmk_booking ON mmk_booking.boat_id = boats_apis_sych.mmk_id WHERE boats_apis_sych.sedna_id = ' +boatid+ ' AND  YEAR(dateFrom) = '+year+' AND MONTH(dateFrom) = '+month+' AND mmk_booking.status = 1 ORDER BY `mmk_booking`.`dateFrom` ASC')
            mmk = cursor.fetchall()

            cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN nausys_boats_bookings ON nausys_boats_bookings.boat_id = boats_apis_sych.nausys WHERE boats_apis_sych.sedna_id = ' +boatid+ ' AND  YEAR(periodFrom) = '+year+' AND MONTH(periodFrom) = '+month+'  ORDER BY `nausys_boats_bookings`.`periodFrom` ASC')
            nausys = cursor.fetchall()


            json_data = []
            for result in sedna:
                content = {"book_id":result[0], "start": result[3], "end": result[4]}
                json_data.append(content)

            json_data_mmk = []
            for result_mmk in mmk:
                content_mmk = {"start": result_mmk[9], "end": result_mmk[10]}
                json_data_mmk.append(content_mmk)
            json_data_nausys = []
            for result_nausys in nausys:
                content_nausys = {"start": result_nausys[9], "end": result_nausys[10], "status": result_nausys[8] }
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


@app.route('/nausys_get_boats/',  methods=['GET'])

def nausys_get_boats():
    import requests
    import json
    boats_bookings = boat_bookings()
    boats = json.loads(boats_bookings)




    return jsonify(boats["reservations"])





@app.route('/nausys_import_boats/',  methods=['GET'])
def nausys_import_boats():
    import requests
    import json
    boats = get_nausys_boats()
    json_boats = json.loads(boats)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()


            for item in json_boats["yachts"]:
                sql = "INSERT INTO `nausys_boats` (`boat_id`, `name`) VALUES (%s, %s);"
                val = (item['id'], item['name'])
                cursor.execute(sql, val)

                conn.commit()

    except Error as e:
        print(e)
    return jsonify(json_boats["yachts"])

def boat_bookings():
    import requests
    import json

    url = "http://ws.nausys.com/CBMS-external/rest/yachtReservation/v6/reservations"

    payload = json.dumps({
        "credentials": {
            "username": "rest@FLY",
            "password": "restFyly761"
        },
        "periodFrom": "01.01.2022",
        "periodTo": "01.01.2023"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    import datetime as dt

    response = requests.request("POST", url, headers=headers, data=payload)
    json_boats = json.loads(response.text)
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()

            for item in json_boats["reservations"]:
                d_dateFrom = int(dt.datetime.strptime(item["periodFrom"], "%d.%m.%Y %H:%M").timestamp())
                # Convert datetime object to date object.
                d_dateFrom_string =  dt.datetime.strptime(item["periodFrom"], "%d.%m.%Y %H:%M").strftime("%Y-%m-%d")
                d_dateTo = int(dt.datetime.strptime(item["periodTo"], "%d.%m.%Y %H:%M").timestamp())
                d_dateTo_string = dt.datetime.strptime(item["periodTo"], "%d.%m.%Y %H:%M").strftime("%Y-%m-%d")
                # Convert datetime object to date object.
                sql = "INSERT INTO `nausys_boats_bookings` (`nausys_booking_id`, `boat_id`, `status`, `periodFrom`, `periodTo`, `update_date`, `hash_dates`) VALUES (%s, %s, %s, %s, %s, current_timestamp(), %s);"
                val = (item['id'], item['yachtId'], item['reservationStatus'], d_dateFrom_string, d_dateTo_string, str(d_dateFrom + d_dateTo))
                cursor.execute(sql, val)

                conn.commit()

    except Error as e:
        print(e)



    return response.text


def get_nausys_boats():
    import requests
    import json

    url = "http://ws.nausys.com/CBMS-external/rest/catalogue/v6/yachts/988432"

    payload = json.dumps({
        "username": "rest@FLY",
        "password": "restFyly761"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text
@app.route('/login/',  methods=['POST'])

def login():
    username = request.args.get("email", None)
    password = request.args.get("password", None)
    import requests
    import json

    data = {'token': "testtt", 'refreshToken': "testtt"}
    print(data)
    return jsonify(data)


@app.route('/crew_boats_update/',  methods=['POST'])

def crew_boats_update():

    return "<h1>Welcome to our server !!</h1>"



@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == "__main__":
    app.run()
