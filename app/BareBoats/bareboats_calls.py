import json
import mysql.connector as mysql
from flask import jsonify
from mysql.connector import Error
from app.BareBoats.bareboats_sych import BareBoats_sych


class BareBoats:
    def __init__(self):
        pass

    def get_logs(self):
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM `sedna_logs` ORDER BY `sedna_logs`.`create_at` DESC LIMIT 50")
                row_headers = [x[0] for x in cursor.description]  # this will extract row headers
                rv = cursor.fetchall()
                json_data = []
                for result in rv:
                    json_data.append(dict(zip(row_headers, result)))
                return jsonify(json_data)
        except Error as e:
            return (e)



    def get_bareboat_plans(self, boatid):
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM `bare_boat_plans` WHERE `plan_url` is NOT NULL AND boat_id=' + boatid)

                rv = cursor.fetchall()
                json_data = []
                for result in rv:
                    content = {"boat_id": result[1], "plan_url": result[2]}
                    json_data.append(content)
                json_output = json.dumps(rv)
                logs = BareBoats_sych()
                logs.sedna_logs_import("Synch Plan: " + boatid, "Plan import to Website")
                return jsonify( json_data)

        except Error as e:
            return (e)

    #Get Boat Extras By ID
    def get_bareboat_extras(self, boatid):

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
                    content = {"id_opt": result[1], "id_opt_bt": result[2], "name": result[3], "price": result[4],
                               "per": result[5]}
                    json_data.append(content)
                    logs = BareBoats_sych()
                    logs.sedna_logs_import("Synch Data: " + boatid, "Data import to Website")

                return jsonify(json_data)

        except Error as e:
            return (e)

    #Get Boat Amenities For all Boats
    def get_bareboat_amenities(self):

        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM boats')
                boats = cursor.fetchall()
                json_data = []


                cursor.execute('SELECT DISTINCT `topic` FROM `boat_characteristics_bare`')
                topics = cursor.fetchall();

                for boat in boats:
                    content_obg = []
                    for  idx, topic in enumerate(topics):
                        cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                            boat[2]) + '" and topic = "' + topic[0] + '";')
                        rv = cursor.fetchall()

                        html = "<ul>"
                        for result in rv:
                            html = html + "<li>" + result[3] + "  " + result[4] + "  " + result[5] + "</li>"
                        html = html + "</ul>"

                        content_obg.append({topic[0]: html})
                    print(content_obg)
                    json_data.append(json.dumps(content_obg))





            return jsonify(json_data)

        except Error as e:
            return (e)

    #Get Boat Amenities Per Boat
    def get_bareboat_amenities_boat(self, boatid):
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()

                json_data = []

                cursor.execute('SELECT DISTINCT `topic` FROM `boat_characteristics_bare`')
                topics = cursor.fetchall();


                content_obg = {}
                for idx, topic in enumerate(topics):
                    cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                        boatid) + '" and topic = "' + topic[0] + '";')
                    rv = cursor.fetchall()

                    html = "<ul>"

                    for result in rv:
                        if result[4]:
                            divider_1 = " : "
                        else:
                            divider_1 = ""
                        html = html + "<li>" + result[3] + divider_1 + result[4] + " " + result[5] + "</li>"
                    html = html + "</ul>"

                    content_obg[topic[0]] = html
                print(content_obg)

            j = json.dumps(content_obg)
            logs = BareBoats_sych()
            logs.sedna_logs_import("Synch Amenities: "+boatid, "Amenities import to Website")
            return jsonify(content_obg)

        except Error as e:
            return (e)

    #Get All Bare Boats Characteristics
    def get_bareboat_characteristics(self):

        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM boats LEFT JOIN boat_characteristics on boat_characteristics.boat_id = boats.boat_id LEFT JOIN boats_bases on boats_bases.boat_id = boats.boat_id WHERE boat_characteristics.crew = "Bare Boat";')

                rv = cursor.fetchall()
                json_data = []
                for result in rv:
                    content = {"name": result[1], "id": result[2], "bt_type": result[5], "model": result[7],
                               "widthboat": result[8], "nbdoucabin": result[9], "nbsimcabin": result[10],
                               "nbper": result[11], "nbbathroom": result[12], "buildyear": result[13],
                               "std_model": result[14], "builder": result[15], "widthboat_feet": result[16],
                               "bt_comment": result[17], "port": result[21], "port_id": result[22]}
                    json_data.append(content)
                return jsonify(json_data)

        except Error as e:
            return (e)

    # Get All Bare Boats Characteristics Pre Boat
    def get_bareboat_characteristics_boat(self, boatid):
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM boats LEFT JOIN boat_characteristics on boat_characteristics.boat_id = boats.boat_id LEFT JOIN boats_bases on boats_bases.boat_id = boats.boat_id WHERE boat_characteristics.crew = "Bare Boat" AND boats.boat_id = "' + str(
                        boatid) + '";')

                rv = cursor.fetchall()
                json_data = []
                for result in rv:
                    content = {"name": result[1], "id": result[2], "bt_type": result[5], "model": result[7],
                               "widthboat": result[8], "nbdoucabin": result[9], "nbsimcabin": result[10],
                               "nbper": result[11], "nbbathroom": result[12], "buildyear": result[13],
                               "std_model": result[14], "builder": result[15], "widthboat_feet": result[16],
                               "bt_comment": result[17], "port": result[21], "port_id": result[22]}
                    json_data.append(content)
                    logs = BareBoats_sych()
                    logs.sedna_logs_import("Synch Data: " + boatid, "Data import to Website")
                return jsonify(json_data)

        except Error as e:
            return (e)

    #Get All Bare Boats Images
    def get_bareboat_images_boat(self, boatid):

        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM boat_images WHERE boat_id = ' + str(boatid) + ';')

                rv = cursor.fetchall()
                json_data = []
                content_obg = {}
                for id, result in enumerate(rv):

                    if(result[3] == "header") :
                        content_obg['header'] = result[2]
                    else:
                        content_obg['image_'+str(id)] = result[2]


                    json_data.append(content_obg)
                    logs = BareBoats_sych()
                    logs.sedna_logs_import("Synch Images: " + boatid, "Images import to Website")
                return jsonify(content_obg)

        except Error as e:
            return (e)