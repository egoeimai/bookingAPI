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
        api_url = 'https://fxyachting.com/wp-json/wp/v2/boats?page=1&per_page=10&fleet_ownership=14'

        response = requests.get(api_url)
        pages_count = response.headers['X-WP-TotalPages']
        response_json = response.json()
        print(response_json)
        return  str(pages_count)


    def get_yatchs_fylys(self):
        wordpress_user = "your username"
        wordpress_password = "xxxx xxxx xxxx xxxx xxxx xxxx"
        wordpress_credentials = wordpress_user + ":" + wordpress_password
        wordpress_token = base64.b64encode(wordpress_credentials.encode())
        wordpress_header = {'Authorization': 'Basic ' + wordpress_token.decode('utf-8')}
        api_url = 'https://fxyachting.com/wp-json/wp/v2/boats?page=1&per_page=10&fleet_ownership=13'

        response = requests.get(api_url)
        pages_count = response.headers['X-WP-TotalPages']
        response_json = response.json()
        print(response_json)
        return  str(pages_count)

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
        print(response_json['id'])
        return response_json['id']

    def create_yatchs_import(self):
        import uuid
        uniq = uuid.uuid4().hex[:6].upper()
        api_url = 'https://fxyachting.com/wp-json/wp/v2/boats?page=1&per_page=10&fleet_ownership=14'

        response = requests.get(api_url)
        pages_count = response.headers['X-WP-TotalPages']
        response_json = response.json()
        str(pages_count)
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly', password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                sqls = "INSERT INTO `other_synch` (`hash`, `total`, `step`, `finished`, `created`) VALUES (%s, %s, %s, '0', current_timestamp());"
                vals = (uniq,  str(pages_count), 0)
                cursor.execute(sqls, vals)
                conn.commit()
            return str(uniq)
        except Error as e:
            return (e)

    def update_yatchs_fylys(self):
        import uuid
        uniq = uuid.uuid4().hex[:6].upper()
        api_url = 'https://fxyachting.com/wp-json/wp/v2/boats?page=1&per_page=10&fleet_ownership=13'

        response = requests.get(api_url)
        pages_count = response.headers['X-WP-TotalPages']
        response_json = response.json()
        str(pages_count)
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly', password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                sqls = "INSERT INTO `other_synch` (`hash`, `total`, `step`, `working`,`finished`, `created`) VALUES (%s, %s, %s, %s, '0', current_timestamp());"
                vals = (uniq,  str(pages_count), 1, 0)
                cursor.execute(sqls, vals)
                conn.commit()

                #self.step_yatchs_import_fyly()
            return str(uniq)

        except Error as e:
            return (e)

    def update_yatchs_fylys_bulk(self, boatids, action):
        import uuid
        uniq = uuid.uuid4().hex[:6].upper()
        api_url = 'https://fxyachting.com/wp-json/wp/v2/boats?page=1&per_page=10&fleet_ownership=13'

        response = requests.get(api_url)
        pages_count = response.headers['X-WP-TotalPages']
        response_json = response.json()
        str(pages_count)
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                sqls = "INSERT INTO `other_synch` (`hash`, `total`, `step`, `working`,  `action`, `finished`, `created`) VALUES (%s, %s, %s, %s, %s, '0', current_timestamp());"
                vals = (uniq, str(pages_count), 1, 0, str(action))
                cursor.execute(sqls, vals)
                conn.commit()

                # self.step_yatchs_import_fyly()
            return str(uniq)

        except Error as e:
            return (e)

    def step_yatchs_import_fyly(self, action):
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM `other_synch` WHERE `finished` = 0 AND `working` = 0 ORDER BY `created` DESC LIMIT 1;')
                rv = cursor.fetchall()
                cursor.execute("UPDATE `other_synch` SET `working` = '1'  WHERE `other_synch`.`synch_id` = " + str(rv[0][0]))
                conn.commit()

                if rv[0][2] >= rv[0][3]:
                    api_url = 'https://fxyachting.com/wp-json/wp/v2/boats?page=' + str(rv[0][3]) + '&per_page=10&fleet_ownership=13&orderby=date'
                    response = requests.get(api_url)
                    response_json = response.json()
                    print(response_json)
                    for boats in response_json:


                        url = "https://fxyachting.com/wp-json/updateboats/v1/boat/" + str(boats['id']) + "?action=" + str(action)

                        payload = {}
                        headers = {}

                        response = requests.request("GET", url, headers=headers, data=payload)

                        #print(response.text)


                        print(boats['id'])
                    cursor.execute("UPDATE `other_synch` SET `step` = " + str(rv[0][3]+1) + " WHERE `other_synch`.`synch_id` = " + str(rv[0][0]))
                    conn.commit()
                    cursor.execute(
                        "UPDATE `other_synch` SET `working` = '0'  WHERE `other_synch`.`synch_id` = " + str(rv[0][0]))
                    conn.commit()
                    step = str(rv[0][3]+1) + ' / ' + str(rv[0][2])
                    return step

                if rv[0][2] < rv[0][3]:
                    cursor.execute("UPDATE `other_synch` SET `finished` = '1'  WHERE `other_synch`.`synch_id` = " + str(rv[0][0]))
                    conn.commit()
                    return str("Finished")



        except Error as e:
            return (e)

