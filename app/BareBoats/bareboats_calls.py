from flask import Flask, request, render_template, jsonify
import mysql.connector as mysql
from mysql.connector import Error
from flask_cors import CORS
import json
from app.crew_boats_update import crew_update
import smtplib, ssl

class BareBoats:
    def __init__(self):
        pass

    def get_bareboat_plans(self):
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
                for boat in boats:
                    content = ""
                    cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                        boat[2]) + '" and topic = "Layout";')
                    rv = cursor.fetchall()

                    html = "<ul>"
                    for result in rv:
                        html = html + "<li>" + result[3] + " : " + result[4] + "</li>"
                    html = html + "</ul>"

                    cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                        boat[2]) + '" and topic = "Amenities";')
                    rv = cursor.fetchall()
                    amenities = "<ul>"
                    for result in rv:
                        amenities = amenities + "<li>" + result[3] + "</li>"
                    amenities = amenities + "</ul>"

                    cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                        boat[2]) + '" and topic = "Characteristics";')
                    rv = cursor.fetchall()
                    Characteristics = "<ul>"
                    for result in rv:
                        Characteristics = Characteristics + "<li>" + result[3] + " : " + result[4] + " " + result[
                            5] + "</li>"
                    Characteristics = Characteristics + "</ul>"

                    cursor.execute(
                        'SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                            boat[2]) + '" and topic = "Inventory";')
                    rv = cursor.fetchall()
                    Inventory = "<ul>"
                    for result in rv:
                        Inventory = Inventory + "<li>" + result[3] + "</li>"
                    Inventory = Inventory + "</ul>"

                    cursor.execute(
                        'SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                            boat[2]) + '" and topic = "Safety Equipment";')
                    rv = cursor.fetchall()
                    Safety_Equipment = "<ul>"
                    for result in rv:
                        Safety_Equipment = Safety_Equipment + "<li>" + result[3] + "</li>"
                    Safety_Equipment = Safety_Equipment + "</ul>"

                    cursor.execute('SELECT plan_url FROM `bare_boat_plans` WHERE `boat_id` = "' + str(boat[2]) + '";')
                    rv_plan = cursor.fetchall()

                    content = {"id": boat[2], "layout": html, "amenities": amenities,
                               "Characteristics": Characteristics, "Inventory": Inventory,
                               "Safety_Equipment": Safety_Equipment, "plans": rv_plan[0]}
                    json_data.append(content)

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

                content = ""
                cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                    boatid) + '" and topic = "Layout";')
                rv = cursor.fetchall()

                html = "<ul>"
                for result in rv:
                    html = html + "<li>" + result[3] + " : " + result[4] + "</li>"
                html = html + "</ul>"

                cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                    boatid) + '" and topic = "Amenities";')
                rv = cursor.fetchall()
                amenities = "<ul>"
                for result in rv:
                    amenities = amenities + "<li>" + result[3] + "</li>"
                amenities = amenities + "</ul>"

                cursor.execute('SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                    boatid) + '" and topic = "Characteristics";')
                rv = cursor.fetchall()
                Characteristics = "<ul>"
                for result in rv:
                    Characteristics = Characteristics + "<li>" + result[3] + " : " + result[4] + " " + result[
                        5] + "</li>"
                Characteristics = Characteristics + "</ul>"

                cursor.execute(
                    'SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                        boatid) + '" and topic = "Inventory";')
                rv = cursor.fetchall()
                Inventory = "<ul>"
                for result in rv:
                    Inventory = Inventory + "<li>" + result[3] + "</li>"
                Inventory = Inventory + "</ul>"

                cursor.execute(
                    'SELECT * FROM `boat_characteristics_bare` WHERE `boat_id` = "' + str(
                        boatid) + '" and topic = "Safety Equipment";')
                rv = cursor.fetchall()
                Safety_Equipment = "<ul>"
                for result in rv:
                    Safety_Equipment = Safety_Equipment + "<li>" + result[3] + "</li>"
                Safety_Equipment = Safety_Equipment + "</ul>"

                cursor.execute('SELECT plan_url FROM `bare_boat_plans` WHERE `boat_id` = "' + str(boatid) + '";')
                rv_plan = cursor.fetchall()
                if (len(rv_plan) > 0):
                    plan = rv_plan[0]
                else:
                    plan = ""


                content = {"id": boatid, "layout": html, "amenities": amenities, "Characteristics": Characteristics,
                           "Inventory": Inventory, "Safety_Equipment": Safety_Equipment, "plans": plan}
                json_data.append(content)

            return jsonify(json_data)

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
                return jsonify(json_data)

        except Error as e:
            return (e)

    #Get All Bare Boats Characteristics
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
                for result in rv:
                    content = {"image": result[2]}
                    json_data.append(content)
                return jsonify(json_data)

        except Error as e:
            return (e)