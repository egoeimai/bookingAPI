from flask import Flask, request, render_template, jsonify
import mysql.connector as mysql
from mysql.connector import Error
import hashlib
import requests
import base64

class fxyatching:


    def __init__(self):
        pass


    def get_yatchs(self):
        wordpress_user = "your username"
        wordpress_password = "xxxx xxxx xxxx xxxx xxxx xxxx"
        wordpress_credentials = wordpress_user + ":" + wordpress_password
        wordpress_token = base64.b64encode(wordpress_credentials.encode())
        wordpress_header = {'Authorization': 'Basic ' + wordpress_token.decode('utf-8')}
        api_url = 'https://fxyachting.com/wp-json/wp/v2/boats'
        response = requests.get(api_url)
        response_json = response.json()
        print(response_json)
        return  str(response_json)

    def create_yatchs(self, boat_name, sedna_id):
        wordpress_user = "restapi_user"
        wordpress_password = "3bJ7 rySR Hl2O QBM2 2A4q Bvp9"
        wordpress_credentials = wordpress_user + ":" + wordpress_password
        wordpress_token = base64.b64encode(wordpress_credentials.encode())
        wordpress_header = {'Authorization': 'Basic ' + wordpress_token.decode('utf-8')}
        api_url = 'https://fxyachting.com/wp-json/wp/v2/boats'


        data = {
            'type': 'boats',
            'title': boat_name,
            'status': 'publish',
            'fleet_ownership': 14,
            "terms": {
                "fleet_ownership": 14
            },
            "acf": {
                "sedna_id": sedna_id
            },


            'content': 'This is the content of the post'
        }
        response = requests.post(api_url, headers=wordpress_header, json=data)

        response_json = response.json()
        print(response_json)
        return  str(response)