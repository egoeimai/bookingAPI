
from flask import Flask, request, render_template, jsonify
import mysql.connector as mysql
from mysql.connector import Error
from flask_cors import CORS
import json

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
                content = {"name": result[1], "id": result[3], "bt_type": result[2], "widthboat": result[6], "widthboatft": result[7], "cabins": result[10], "nbper": result[9], "buildyear": result[8], "builder": result[14], "crew": result[11], "lowprice": result[12], "highprice": result[13], "mainimage":result[18], "extraimages":result[19], "port":result[15], "num_crew": result[22], "captainname": result[23], "captainnation": result[24],
                           "captainborn": result[25], "captainlang": result[26], "crewname": result[27],
                           "crewtitle": result[28], "crewnation": result[29], "crewborn": result[30],
                           "crewtext": result[31], "image1": result[32], "image2": result[33], "video_url": result[36], }
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)



@app.route('/get_crewd_boat/',  methods=['GET'])
def get_crewd_boat():
    boatid = request.args.get("boatid", None)

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM `crew_boats` LEFT JOIN crew_boats_basic ON crew_boats.boat_id = crew_boats_basic.boat_id LEFT JOIN crew_images_boats ON crew_images_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_boat_crewd on crew_boat_crewd.boat_id = crew_boats.boat_id LEFT JOIN crew_video_boats ON crew_video_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_amenties ON crew_amenties.boat_id = crew_boats.boat_id LEFT JOIN crew_characteristics ON crew_characteristics.boat_id = crew_boats.boat_id LEFT JOIN crew_water_sports ON crew_water_sports.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtothertoys ON crew_yachtothertoys.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtotherentertain ON crew_yachtotherentertain.boat_id = crew_boats.boat_id WHERE `boat_id` = ' + boatid +';')

            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"name": result[1], "id": result[3], "bt_type": result[2], "widthboat": result[6], "widthboatft": result[7], "cabins": result[10], "nbper": result[9], "buildyear": result[8], "builder": result[14], "crew": result[11], "lowprice": result[12], "highprice": result[13], "mainimage":result[18], "extraimages":result[19], "port":result[15], "num_crew": result[22], "captainname": result[23], "captainnation": result[24],
                           "captainborn": result[25], "captainlang": result[26], "crewname": result[27],
                           "crewtitle": result[28], "crewnation": result[29], "crewborn": result[30],
                           "crewtext": result[31], "image1": result[32], "image2": result[33], "video_url": result[36], }
                json_data.append(content)
            return jsonify(json_data)

    except Error as e:
        return (e)

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


@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == "__main__":
    app.run()
