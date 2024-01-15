from flask import Flask, request, render_template, jsonify
import mysql.connector as mysql
from mysql.connector import Error
import hashlib

class Crew_bookings:


    def __init__(self):
        pass

    def select_free_bookings(self, start, end):
        import json
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()

                cursor.execute('SELECT * FROM crew_boats_select LEFT JOIN crew_images_boats ON crew_images_boats.boat_id = crew_boats_select.crew_id LEFT JOIN crew_boats_basic ON crew_boats_basic.boat_id = crew_boats_select.crew_id LEFT JOIN crew_characteristics ON crew_characteristics.boat_id = crew_boats_select.crew_id LEFT JOIN crewed_areas ON crewed_areas.boat_id = crew_boats_select.crew_id WHERE crew_boats_select.crew_id NOT IN (SELECT crew_bookings.boat_id FROM crew_bookings JOIN crew_boats_select ON crew_bookings.boat_id = crew_boats_select.crew_id WHERE  "' + start + '" < enda_date AND "' + end + '" > start_date) AND crew_boats_select.is_fyly = 1')
                row_headers = [x[0] for x in cursor.description]  # this will extract row headers
                rv = cursor.fetchall()
                json_data = []
                for result in rv:
                    json_data.append(dict(zip(row_headers, result)))
                return jsonify(json_data)

        except Error as e:
            return (e)


    def get_history_predefine(self):
        import json
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()

                cursor.execute('SELECT * FROM `predifine` ')
                row_headers = [x[0] for x in cursor.description]  # this will extract row headers
                rv = cursor.fetchall()
                json_data = []
                for result in rv:
                    json_data.append(dict(zip(row_headers, result)))
                return jsonify(json_data)

        except Error as e:
            return (e)

    def crew_update_bookings(self):
        token = ""
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute('TRUNCATE TABLE crew_bookings;')

        except Error as e:
            print(e)

        import requests

        cursor.execute('SELECT crew_id FROM crew_boats_select WHERE is_fyly = 1')
        row_headers = [x[0] for x in cursor.description]  # this will extract row headers
        rv = cursor.fetchall()
        Boat_log = ""
        for boats in rv:
            reqUrl = "http://www.centralyachtagent.com/snapins/json-calendar.php?idin=" +  str(boats[0]) + "&user=1318"
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
                    hash_val_booking = (booking_date['yachtBookId'], booking_date['yachtStartDateNum'], booking_date['yachtEndDateNum'], booking_date['yachtBookDesc'])
                    sql_extra = "INSERT INTO `crew_bookings`(`boat_id`, `start_date`, `enda_date`, `book_description`, `hash`)  VALUES( %s, %s, %s, %s, %s);"
                    val_booking = (booking_date['yachtBookId'], booking_date['yachtStartDateNum'], booking_date['yachtEndDateNum'], booking_date['yachtBookDesc'], hashlib.md5(str(hash_val_booking).encode("utf-8")).hexdigest())

                    cursor.execute(sql_extra, val_booking)
                    conn.commit()
        return "Complete"

    def crew_get_bookings(self, boat_id):
        from  datetime import datetime
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()

                cursor.execute('SELECT * FROM crew_bookings WHERE boat_id =' + str(boat_id))
                row_headers = [x[0] for x in cursor.description]  # this will extract row headers
                rv = cursor.fetchall()
                json_data = []
                for result in rv:
                    content = {"from": result[2].strftime('%Y-%m-%d'), "to": result[3].strftime('%Y-%m-%d'), "middayCheckout": "false"}
                    json_data.append(content)
                return jsonify(json_data)

        except Error as e:
            return (e)




