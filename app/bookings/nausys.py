from flask import Flask, request, render_template, jsonify
import mysql.connector as mysql
from mysql.connector import Error
import hashlib

class Nausys:


    def __init__(self):
        pass


    def insert_boat_bookings(self):
        import requests
        import json
        import datetime

        today = datetime.date.today()
        first = today.replace(day=1)
        last_month = first - datetime.timedelta(days=1)

        url = "http://ws.nausys.com/CBMS-external/rest/yachtReservation/v6/reservations"

        payload = json.dumps({
            "credentials": {
                "username": "rest@FLY",
                "password": "restFyly761"
            },
            "periodFrom": str(last_month.strftime("%d.%m.%Y")),
            "periodTo": "31.12.2023"
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
                cursor.execute('TRUNCATE TABLE nausys_boats_bookings;')

                for item in json_boats["reservations"]:
                    d_dateFrom = int(dt.datetime.strptime(item["periodFrom"], "%d.%m.%Y %H:%M").timestamp())
                    # Convert datetime object to date object.
                    d_dateFrom_string =  dt.datetime.strptime(item["periodFrom"], "%d.%m.%Y %H:%M").strftime("%Y-%m-%d")
                    d_dateTo = int(dt.datetime.strptime(item["periodTo"], "%d.%m.%Y %H:%M").timestamp())
                    d_dateTo_string = dt.datetime.strptime(item["periodTo"], "%d.%m.%Y %H:%M").strftime("%Y-%m-%d")
                    # Convert datetime object to date object.
                    sql = "INSERT INTO `nausys_boats_bookings` (`nausys_booking_id`, `boat_id`, `status`, `periodFrom`, `periodTo`, `update_date`, `hash_dates`) VALUES (%s, %s, %s, %s, %s, current_timestamp(), %s);"
                    val = (item['id'], item['yachtId'], item['reservationStatus'], d_dateFrom_string, d_dateTo_string, hashlib.md5(str(d_dateFrom_string + d_dateTo_string).encode("utf-8")).hexdigest())
                    cursor.execute(sql, val)

                    conn.commit()

        except Error as e:
            print(e)

        return response.text

    def nausys_import_boats(self):
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
        boats = response.text
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
        return json_boats["yachts"]

