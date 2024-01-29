from flask import Flask, request, render_template, jsonify
import mysql.connector as mysql
from mysql.connector import Error
import concurrent.futures
from flask_cors import CORS
import json
from app.crew_boats_update import crew_update
import smtplib, ssl


class BareBoats_sych:
    def __init__(self):
        pass

    def bareboats_sych_plans(self):
        token = ""
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute('TRUNCATE TABLE bare_boat_plans;')
                import requests

                reqUrl = "https://api.sednasystem.com/API/getaccess.asp?l=Zonepage&p=Zonepage2022@&appname=apiboatcharter"

                headersList = {
                    "Accept": "*/*",
                    "User-Agent": "opa36",
                    "connection": "Keep-alive"
                }

                payload = ""

                response = requests.request("GET", reqUrl, data=payload, headers=headersList)
                import xml.etree.ElementTree as ET

                xml = ET.fromstring(response.text)

                for holiday in xml.findall('token'):
                    print(holiday.attrib['authtoken'])
                    token = holiday.attrib['authtoken']

        except Error as e:
            print(e)

        reqUrl = "https://api.sednasystem.com/API/getBts5.asp?token=" + token + "&appname=apiboatcharter"

        headersList = {
            "Accept": "*/*",
            "User-Agent": "opa36",
            "connection": "Keep-alive"
        }

        payload = ""
        mycursor = conn.cursor()
        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        import xml.etree.ElementTree as ET
        xml = ET.fromstring(response.text)
        with open("output.xml", "w") as f:
            f.write(response.text)
        for boat in xml.findall('boat'):

            plans = boat.findall('plans')
            for plan in plans:
                for plan_inner in plan:
                    print(plan_inner)
                    sqls_plans = "INSERT INTO `bare_boat_plans` (`boat_id`, `plan_url`) VALUES (%s, %s);"
                    plans_vals = (
                        boat.attrib['id_boat'], plan_inner.attrib['link'])
                    mycursor.execute(sqls_plans, plans_vals)
                    conn.commit()
        return "success"

    def baraboats_sych_amenities(self, duration):
        token = ""
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute('TRUNCATE TABLE boat_characteristics_bare;')
                import requests

                reqUrl = "https://api.sednasystem.com/API/getaccess.asp?l=Zonepage&p=Zonepage2022@&appname=apiboatcharter"

                headersList = {
                    "Accept": "*/*",
                    "User-Agent": "opa36",
                    "connection": "Keep-alive"
                }

                payload = ""

                response = requests.request("GET", reqUrl, data=payload, headers=headersList)
                import xml.etree.ElementTree as ET

                xml = ET.fromstring(response.text)

                for holiday in xml.findall('token'):
                    print(holiday.attrib['authtoken'])
                    token = holiday.attrib['authtoken']

        except Error as e:
            print(e)

        reqUrl = "https://api.sednasystem.com/API/getBts5.asp?token=" + token + "&appname=apiboatcharter"

        headersList = {
            "Accept": "*/*",
            "User-Agent": "opa36",
            "connection": "Keep-alive"
        }

        payload = ""
        mycursor = conn.cursor()
        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        import xml.etree.ElementTree as ET
        xml = ET.fromstring(response.text)

        try:
            for boat in xml.findall('boat'):

                characteristics = boat.findall('characteristics')
                for characteristic_topic in characteristics:
                    characteristic = characteristic_topic.findall('characteristic_topic')
                    for characteristic_inner in characteristic:
                        # print(characteristic_inner.attrib['topic'])
                        for characteristic_list in characteristic_inner:
                            print(characteristic_list.attrib['name'])
                            sqls_characteristic = "INSERT INTO `boat_characteristics_bare`(`boat_id`, `topic`, `name`, `qnt`, `unit`, `hash`) VALUES(%s, %s, %s, %s, %s, %s);"
                            characteristic_vals = (boat.attrib['id_boat'], characteristic_inner.attrib['topic'],
                                                   characteristic_list.attrib['name'],
                                                   characteristic_list.attrib['quantity'],
                                                   characteristic_list.attrib['unit'], hash(characteristic_list))
                            mycursor.execute(sqls_characteristic, characteristic_vals)
                            conn.commit()

            self.send_success_email("Update Import Data", "The Data of BareBoats has been updated")
            print("Background task completed.")

        except:
            self.send_success_email("Update Import Data Faild", "The Data of BareBoats has been Faild")

    def bareboats_sych_boat_extras(self, duration):
        token = ""
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()

                print("You're connected to database: ", record)
                cursor.execute('TRUNCATE TABLE boats;')
                cursor.execute('TRUNCATE TABLE boats_bases;')
                cursor.execute('TRUNCATE TABLE boat_characteristics;')
                import requests
                reqUrl = "https://api.sednasystem.com/API/getaccess.asp?l=Zonepage&p=Zonepage2022@&appname=apiboatcharter"

                headersList = {
                    "Accept": "*/*",
                    "User-Agent": "opa36",
                    "connection": "Keep-alive"
                }

                payload = ""

                response = requests.request("GET", reqUrl, data=payload, headers=headersList)
                import xml.etree.ElementTree as ET
                xml = ET.fromstring(response.text)
                for boat in xml.findall('token'):
                    print(boat.attrib['authtoken'])
                    token = boat.attrib['authtoken']
        except Error as e:
            print(e)

        reqUrl = "https://api.sednasystem.com/API/getBts5.asp?token=" + token + "&appname=apiboatcharter"

        headersList = {
            "Accept": "*/*",
            "User-Agent": "opa36",
            "connection": "Keep-alive"
        }

        payload = ""
        mycursor = conn.cursor()
        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        import xml.etree.ElementTree as ET
        xml = ET.fromstring(response.text)
        try:
            for boat in xml.findall('boat'):
                sql = "INSERT INTO boats (boat_name, boat_id) VALUES (%s, %s)"
                val = (boat.attrib['name'], boat.attrib['id_boat'])
                mycursor.execute(sql, val)
                conn.commit()
                print(mycursor.rowcount, "record inserted.")
                sqls = "INSERT INTO `boat_characteristics` (`boat_id`, `bt_type`, `crew`, `model`, `widthboat`, `nbdoucabin`, `nbsimcabin`, `nbper`, `nbbathroom`, `buildyear`, `std_model`, `builder`, `widthboat_feet`, `bt_comment`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                vals = (boat.attrib['id_boat'], boat.attrib['bt_type'], boat.attrib['crew'], boat.attrib['model'],
                        boat.attrib['widthboat'], boat.attrib['nbdoucabin'], boat.attrib['nbsimcabin'],
                        boat.attrib['nbper'], boat.attrib['nbbathroom'], boat.attrib['buildyear'],
                        boat.attrib['std_model'],
                        boat.attrib['builder'], boat.attrib['widthboat_feet'], boat.attrib['bt_comment'])
                mycursor.execute(sqls, vals)

                homeports = boat.findall('homeport')
                for homeport in homeports:
                    sql_bases = "INSERT INTO boats_bases (boat_id, destination_id, destination_name, id_tbf1) VALUES (%s, %s, %s, %s)"
                    val_bases = (
                        boat.attrib['id_boat'], homeport.attrib['id_base'], homeport.attrib['name'],
                        homeport.attrib['id_tbf1'])
                    mycursor.execute(sql_bases, val_bases)

                conn.commit()
            self.send_success_email("Update Import Data", "The Data of BareBoats has been updated")
            print("Background task completed.")

        except:
            self.send_success_email("Update Import Data Faild", "The Data of BareBoats has been Faild")

    def bareboasts_sych_boat_images(self, duration):
        import requests
        import mysql.connector as mysql
        from mysql.connector import Error
        from PIL import Image
        token = ""
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute('TRUNCATE TABLE boat_images;')
                import requests

                reqUrl = "https://api.sednasystem.com/API/getaccess.asp?l=Zonepage&p=Zonepage2022@&appname=apiboatcharter"

                headersList = {
                    "Accept": "*/*",
                    "User-Agent": "opa36",
                    "connection": "Keep-alive"
                }

                payload = ""

                response = requests.request("GET", reqUrl, data=payload, headers=headersList)
                import xml.etree.ElementTree as ET

                xml = ET.fromstring(response.text)

                for holiday in xml.findall('token'):
                    print(holiday.attrib['authtoken'])
                    token = holiday.attrib['authtoken']

        except Error as e:
            print(e)

        reqUrl = "https://api.sednasystem.com/API/getBts5.asp?token=" + token + "&appname=apiboatcharter"

        headersList = {
            "Accept": "*/*",
            "User-Agent": "opa36",
            "connection": "Keep-alive"
        }

        payload = ""
        mycursor = conn.cursor()
        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        import xml.etree.ElementTree as ET
        xml = ET.fromstring(response.text)
        try:

            for boat in xml.findall('boat'):
                images = boat.findall('picts')
                print(type(images))
                for pictures in images:
                    images_inner = pictures.findall('pict')
                    for pictures_inner in images_inner:
                        print(pictures_inner.attrib['link'])
                        sqls_images = "INSERT INTO `boat_images` (`boat_id`, `image_url`, `position`) VALUES (%s, %s, %s);"
                        images_vals = (
                            boat.attrib['id_boat'], pictures_inner.attrib['link'], pictures_inner.attrib['position'])
                        mycursor.execute(sqls_images, images_vals)
                        conn.commit()

            self.send_success_email("Update Import Images", "The Images of BareBoats has been updated")
            print("Background task completed.")

        except:
            self.send_success_email("Update Import Images Faild", "The Images of BareBoats has been Faild")

    def baraboats_sych_prices(self, duration):
        token = ""
        print(f"Starting background task with duration...")
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                cursor.execute('TRUNCATE TABLE boat_prices;')
                import requests

                reqUrl = "https://api.sednasystem.com/API/getaccess.asp?l=Zonepage&p=Zonepage2022@&appname=apiboatcharter"

                headersList = {
                    "Accept": "*/*",
                    "User-Agent": "opa36",
                    "connection": "Keep-alive"
                }

                payload = ""

                response = requests.request("GET", reqUrl, data=payload, headers=headersList)
                import xml.etree.ElementTree as ET

                xml = ET.fromstring(response.text)

                for holiday in xml.findall('token'):
                    print(holiday.attrib['authtoken'])
                    token = holiday.attrib['authtoken']

        except Error as e:
            print(e)

        reqUrl = "https://api.sednasystem.com/API/getBts5.asp?token=" + token + "&appname=apiboatcharter"

        headersList = {
            "Accept": "*/*",
            "User-Agent": "opa36",
            "connection": "Keep-alive"
        }

        payload = ""
        mycursor = conn.cursor()
        response = requests.request("GET", reqUrl, data=payload, headers=headersList)
        import xml.etree.ElementTree as ET
        xml = ET.fromstring(response.text)
        try:
            for boat in xml.findall('boat'):

                prices = boat.findall('prices')
                for price in prices:
                    price_inner = price.findall('price')
                    for price_val in price_inner:
                        print(price_val.attrib['amount'])
                        sqls_price = "INSERT INTO `boat_prices` (`boat_id`, `datestart`, `dateend`, `amount`, `unitamount`) VALUES (%s, %s, %s, %s, %s);"
                        price_vals = (
                            boat.attrib['id_boat'], price_val.attrib['datestart'], price_val.attrib['dateend'],
                            price_val.attrib['amount'], price_val.attrib['unitamount'])
                        mycursor.execute(sqls_price, price_vals)
                        conn.commit()

            self.send_success_email("Update Import Prices", "The prices of BareBoats has been updated")
            print("Background task completed.")
        except:
            self.send_success_email("Update Import Prices Faild", "The prices of BareBoats has been Faild")

    def send_success_email(self, subject_t, text):
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from string import Template

        # check new data type

        username = "development@zonepage.gr"
        password = "Vac51132"
        mail_from = "development@zonepage.gr"
        mail_subject = subject_t
        mail_body = text
        mimemsg = MIMEMultipart()
        mimemsg['From'] = mail_from
        mimemsg['To'] = "nziozas@gmail.com"
        mimemsg['Subject'] = mail_subject
        mimemsg.attach(MIMEText(mail_body, 'plain'))
        connection = smtplib.SMTP(host='smtp.office365.com', port=587)
        connection.starttls()
        connection.login(username, password)
        connection.send_message(mimemsg)
        connection.quit()
