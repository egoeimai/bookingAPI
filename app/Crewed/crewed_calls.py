from flask import Flask, request, render_template, jsonify
import mysql.connector as mysql
from mysql.connector import Error
from flask_cors import CORS
import json
from app.crew_boats_update import crew_update
import smtplib, ssl

class CrewedBoats:
    def __init__(self):
        pass

    def get_all_crew_boasts(self):
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT * FROM `crew_boats` LEFT JOIN crew_boats_basic ON crew_boats.boat_id = crew_boats_basic.boat_id LEFT JOIN crew_images_boats ON crew_images_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_boat_crewd on crew_boat_crewd.boat_id = crew_boats.boat_id LEFT JOIN crew_video_boats ON crew_video_boats.boat_id = crew_boats.boat_id LEFT JOIN crew_amenties ON crew_amenties.boat_id = crew_boats.boat_id LEFT JOIN crew_characteristics ON crew_characteristics.boat_id = crew_boats.boat_id LEFT JOIN crew_water_sports ON crew_water_sports.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtothertoys ON crew_yachtothertoys.boat_id = crew_boats.boat_id LEFT JOIN crew_yachtotherentertain ON crew_yachtotherentertain.boat_id = crew_boats.boat_id;')

                rv = cursor.fetchall()
                json_data = []
                for result in rv:
                    content = {"name": result[1], "id": result[3], "bt_type": result[2], "widthboat": result[6],
                               "widthboatft": result[7], "cabins": result[10], "nbper": result[9],
                               "buildyear": result[8], "builder": result[14], "crew": result[11],
                               "lowprice": result[12], "highprice": result[13], "mainimage": result[23],
                               "extraimages": result[24], "port": result[15], "num_crew": result[27],
                               "captainname": result[28], "captainnation": result[29],
                               "captainborn": result[30], "captainlang": result[31], "crewname": result[32],
                               "crewtitle": result[33], "crewnation": result[34], "crewborn": result[35],
                               "crewtext": result[36], "image1": result[37], "image2": result[38],
                               "video_url": result[41], "description": result[16], "price_details": result[17],
                               "locations_details": result[18], "broker_notes": result[19]}
                    json_data.append(content)
                return jsonify(json_data)

        except Error as e:
            return (e)