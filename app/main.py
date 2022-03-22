
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


@app.route('/getboats/',  methods=['GET'])
def getboats():

    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM boats LEFT JOIN boat_characteristics on boat_characteristics.boat_id = boats.boat_id LEFT JOIN boat_characteristics on boat_characteristics.boat_id = boats.boat_id WHERE boat_characteristics.crew = "Bare Boat";')
            row_headers = [x[0] for x in cursor.description]  # this will extract row headers
            rv = cursor.fetchall()
            json_data = []
            for result in rv:
                content = {"name": result[1], "id": result[2], "bt_type": result[5], "model": result[7], "widthboat": result[8], "nbdoucabin": result[9], "nbsimcabin": result[10], "nbper": result[11], "nbbathroom": result[12], "buildyear": result[13], "std_model": result[14], "builder": result[15], "widthboat_feet": result[15], "bt_comment": result[16] }
                json_data.append(content)
            return jsonify(json_data)

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
                content = {"name": result[1], "id": result[2], "destination_name": result[6]}
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

@app.route('/getboat_events/',  methods=['POST'])
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
    return jsonify(args)


@app.route('/sendclient/',  methods=['GET'])
def sendclient():
    name = request.args.get("name", None)
    email = request.args.get("email", None)
    country = request.args.get("country", None)
    tel = request.args.get("tel", None)
    reqUrl = "https://api.sednasystem.com/api/insertclient.asp?name=NikosZiozas&email=nziozas@gmail.com&country=Greece&tel=6974733098&choix=ope&refope=ysy171"

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
