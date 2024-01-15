from app.bookings.nausys import Nausys
from app.bookings.sedna import Sedna
from app.bookings.mmk import MMK
import json
from flask import Flask, request, render_template, jsonify
import mysql.connector as mysql
from mysql.connector import Error
from flask_cors import CORS

class FylyApi:
    def __init__(self):
        pass

    #@app.route('/mmk_import_boats/',  methods=['GET'])
    def mmk_import_boats(self):

        boats_bookings = MMK()
        boats = json.loads(boats_bookings.insert_boat_bookings())
        return jsonify(boats)


    #@app.route('/sedna_import_bookings/',  methods=['GET'])
    def sedna_import_bookings(self):

        boats_bookings = Sedna()
        boats = json.loads(boats_bookings.insert_boat_bookings())
        return jsonify(boats)


    #@app.route('/nausys_sych_bookings/',  methods=['GET'])

    def nausys_sych_bookings(self):

        import json
        boats_bookings =Nausys()
        boats = json.loads(boats_bookings.insert_boat_bookings())
        return jsonify(boats["reservations"])

    """ Sedna To Nausys Sychronize """


    #@app.route('/get_sedna_to_nausys/',  methods=['GET'])
    def get_sedna_to_nausys(self):
        boatid = request.args.get("boatid", None)

        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly', password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM `boats_apis_sych`')
                boats = cursor.fetchall()
                nausys_log = ""
                log_count = 0
                import datetime

                today = datetime.date.today()
                first = today.replace(day=1)
                last_month = first - datetime.timedelta(days=1)

                for result_boats in boats:
                    cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN nausys_boats_bookings ON nausys_boats_bookings.boat_id = boats_apis_sych.nausys WHERE boats_apis_sych.sedna_id = ' + str(result_boats[1]) + ' AND nausys_boats_bookings.status = "RESERVATION" AND nausys_boats_bookings.periodFrom >  "' + str(last_month.strftime("%Y-%m-%d")) + '"')
                    nausys = cursor.fetchall()
                    cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN boats_booking ON boats_booking.boat_id = boats_apis_sych.sedna_id WHERE boats_apis_sych.sedna_id = ' + str(result_boats[1]) + ' AND boats_booking.status = 0 AND boats_booking.datestart > "' + str(last_month.strftime("%Y-%m-%d")) + '"' )
                    sedna = cursor.fetchall()
                    import requests
                    import json

                    if len(nausys) < len(sedna):

                        for result in sedna:
                            exist = 0
                            for i, d in enumerate(nausys):

                                if d[12] == result[10]:
                                    exist = 1

                                    break
                            else:
                                i = -1
                            if exist == 0:
                                if result_boats[3] > 0:
                                    url = "http://ws.nausys.com/CBMS-external/rest/booking/v6/createInfo/"

                                    payload = json.dumps({
                                        "client": {
                                            "name": "FYLY",
                                            "surname": "API",
                                            "company": "false",
                                            "vatNr": "",
                                            "address": "address",
                                            "zip": "",
                                            "city": "",
                                            "countryId": "100116",
                                            "email": "somebody@someone.some",
                                            "phone": "",
                                            "mobile": "",
                                            "skype": ""
                                        },
                                        "credentials": {
                                            "username": "rest@FLY",
                                            "password": "restFyly761"
                                        },
                                        "periodFrom": result[8].strftime('%d.%m.%Y'),
                                        "periodTo": result[9].strftime('%d.%m.%Y'),
                                        "yachtID": result_boats[3],
                                    })

                                    headers = {
                                        'Content-Type': 'application/json'
                                    }

                                    response = requests.request("POST", url, headers=headers, data=payload)

                                    if 'id' in json.loads(response.text):


                                        url = "http://ws.nausys.com/CBMS-external/rest/booking/v6/createBooking"

                                        payload = json.dumps({
                                            "credentials": {
                                                "username": "rest@FLY",
                                                "password": "restFyly761"
                                            },
                                            "id": json.loads(response.text)['id'],
                                            "uuid": json.loads(response.text)['uuid']


                                        })
                                        headers = {
                                            'Content-Type': 'application/json'
                                        }

                                        responses = requests.request("POST", url, headers=headers, data=payload)


                                        message = "<strong> Σφάλμα </strong>: " + json.loads(responses.text)["status"]
                                        print("Σκάφος: " + str(result_boats[3]) + "|" + str(result_boats[4]) + " - Κράτηση:  " + result[8].strftime('%d.%m.%Y') + " - " + result[9].strftime('%Y-%m-%d') + " <br>" + message)
                                        nausys_log = nausys_log + " Σκάφος: " + str(result_boats[3]) + "|" + str(result_boats[4]) + " - Κράτηση:  " + result[8].strftime('%d.%m.%Y') + " - " + result[9].strftime('%Y-%m-%d') + " <br>" + message
                                        log_count = log_count + 1

                                    else :
                                        print("0 ID")

            sql_bases = 'INSERT INTO api_nausys_sych (log, log_count) VALUES (%s, %s);'
            val_bases = (nausys_log, log_count)
            cursor.execute(sql_bases, val_bases)


            conn.commit()

            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            username = "development@zonepage.gr"
            password = "Won14376"
            mail_from = "development@zonepage.gr"
            mail_to = "n.ziozas@zonepage.gr, fyly@fyly.gr"
            mail_subject = "Nausys Log"
            mail_body = "Nausys Log :  " + nausys_log

            mimemsg = MIMEMultipart()
            mimemsg['From'] = mail_from
            mimemsg['To'] = mail_to
            mimemsg['Subject'] = mail_subject
            mimemsg.attach(MIMEText(mail_body, 'html'))
            connection = smtplib.SMTP(host='smtp.office365.com', port=587)
            connection.starttls()
            connection.login(username, password)
            connection.send_message(mimemsg)
            connection.quit()

            return  nausys_log

        except Error as e:
            return (e)


    """ Sedna To MMK Sychronize """

    #@app.route('/get_sedna_to_mmk/',  methods=['GET'])
    def get_sedna_to_mmk(self):
        boatid = request.args.get("boatid", None)

        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly', password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM `boats_apis_sych`')
                boats = cursor.fetchall()
                mmk_log = ""
                log_count = 0
                for result_boas in boats:
                    cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN mmk_booking ON mmk_booking.boat_id = boats_apis_sych.mmk_id WHERE boats_apis_sych.sedna_id = ' + str(result_boas[1]) + ' AND mmk_booking.status = 1')
                    mmk = cursor.fetchall()
                    cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN boats_booking ON boats_booking.boat_id = boats_apis_sych.sedna_id WHERE boats_apis_sych.sedna_id = ' + str(result_boas[1]) + ' AND boats_booking.status = 0;')
                    sedna = cursor.fetchall()
                    import requests
                    import json

                    if len(mmk) < len(sedna):

                        for result in sedna:
                            exist = 0
                            for i, d in enumerate(mmk):

                                if d[15] == result[10]:
                                    exist = 1
                                    break
                            else:
                                i = -1
                            if exist == 0:
                                url = "https://www.booking-manager.com/api/v2/reservation"
                                print(result[9].strftime('%Y-%m-%dT%H:%M:%S.%f%z'))
                                payload = json.dumps({
                                    "dateFrom": result[8].strftime('%Y-%m-%dT%H:%M:%S'),
                                    "dateTo": result[9].strftime('%Y-%m-%dT%H:%M:%S'),
                                    "yachtId": result_boas[2],
                                    "status": 2
                                })
                                headers = {
                                    'Authorization': 'Bearer 837-d6973f84d9b2752274d9695ee411b01176871329d36b12872601a0837b390374104b7fa3542e0aefade6f65835bd09885f372592ddc57b44a2a853602dd03cc2',
                                    'Content-Type': 'application/json'
                                }

                                response = requests.request("POST", url, headers=headers, data=payload)

                                print(response.text)
                                mmk_result = json.loads(response.text)
                                print(mmk_result["id"])
                                message = "<strong> Σφάλμα </strong>: " + response.text
                                if len(response.text) > 192:
                                    message = "<strong>Πέρασε</strong>"

                                print("Σκάφος: " + str(result[2]) + " - Κράτηση:  " + result[8].strftime('%Y-%m-%d') + " - " + result[9].strftime('%Y-%m-%d') + " <br>" + message)
                                mmk_log = mmk_log + "<p>Σκάφος: " +  str(result[2]) + "|" + str(result_boas[4]) + " - Κράτηση:  " + result[8].strftime('%Y-%m-%d') + " - " + result[9].strftime('%Y-%m-%d') + "  <br>" + message + "</p>"
                                log_count = log_count + 1
            #print(log_count)
            sql_bases = 'INSERT INTO api_mmk_sych (log, log_count) VALUES ( %s, %s);'
            val_bases = (mmk_log, log_count)
            cursor.execute(sql_bases, val_bases)

            conn.commit()

            import smtplib
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText

            username = "development@zonepage.gr"
            password = "Won14376"
            mail_from = "development@zonepage.gr"
            mail_to = "n.ziozas@zonepage.gr, fyly@fyly.gr"
            mail_subject = "MMK Log"
            mail_body = "Mmk_log :  " + mmk_log

            mimemsg = MIMEMultipart()
            mimemsg['From'] = mail_from
            mimemsg['To'] = mail_to
            mimemsg['Subject'] = mail_subject
            mimemsg.attach(MIMEText(mail_body, 'html'))
            connection = smtplib.SMTP(host='smtp.office365.com', port=587)
            connection.starttls()
            connection.login(username, password)
            connection.send_message(mimemsg)
            connection.quit()
            return mmk_log

        except Error as e:
            return (e)

    #@app.route('/api_react_date/',  methods=['GET'])
    def api_react_date(self):
        boatid = request.args.get("boatid", None)
        month = request.args.get("month", None)
        year = request.args.get("year", None)


        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM boats_booking WHERE boat_id='+boatid+' AND  YEAR(datestart) = '+year+' AND MONTH(datestart) = '+month+'  AND (status=0 OR status=1) ORDER BY `boats_booking`.`datestart` ASC' )
                row_headers = [x[0] for x in cursor.description]  # this will extract row headers
                sedna = cursor.fetchall()

                cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN mmk_booking ON mmk_booking.boat_id = boats_apis_sych.mmk_id WHERE boats_apis_sych.sedna_id = ' +boatid+ ' AND  YEAR(dateFrom) = '+year+' AND MONTH(dateFrom) = '+month+' AND (mmk_booking.status = 1 OR mmk_booking.status = 2)  ORDER BY `mmk_booking`.`dateFrom` ASC')
                mmk = cursor.fetchall()

                cursor.execute('SELECT * FROM `boats_apis_sych` LEFT JOIN nausys_boats_bookings ON nausys_boats_bookings.boat_id = boats_apis_sych.nausys WHERE boats_apis_sych.sedna_id = ' +boatid+ ' AND  YEAR(periodFrom) = '+year+' AND MONTH(periodFrom) = '+month+'  ORDER BY `nausys_boats_bookings`.`periodFrom` ASC')
                nausys = cursor.fetchall()


                json_data = []
                for result in sedna:
                    if result[2] == 0:
                        content = {"bookid":result[0], "start": result[3], "end": result[4], "status": "RESERVATION"}
                    else:
                        content = {"bookid":result[0], "start": result[3], "end": result[4], "status": "OPTION"}

                    json_data.append(content)

                json_data_mmk = []
                for result_mmk in mmk:
                    if  result_mmk[8] == 1:
                        content_mmk = {"start": result_mmk[9], "end": result_mmk[10], "bookid" : result_mmk[6], "status": "RESERVATION"}
                    else:
                        content_mmk = {"start": result_mmk[9], "end": result_mmk[10], "bookid": result_mmk[6],"status": "OPTION"}
                    json_data_mmk.append(content_mmk)
                json_data_nausys = []
                for result_nausys in nausys:
                    content_nausys = {"start": result_nausys[9], "end": result_nausys[10], "status": result_nausys[8], "bookid" : result_nausys[6] }
                    json_data_nausys.append(content_nausys)

                cursor.execute('SELECT * FROM boats LEFT JOIN boat_characteristics on boat_characteristics.boat_id = boats.boat_id LEFT JOIN boats_bases on boats_bases.boat_id = boats.boat_id WHERE boats.boat_id='+boatid)

                rv_data = cursor.fetchall()
                json_data_rv = []
                for result in rv_data:
                    content_rv = {"name": result[1], "id": result[2], "bt_type": result[5], "model": result[7],
                               "widthboat": result[8], "nbdoucabin": result[9], "nbsimcabin": result[10],
                               "nbper": result[11], "nbbathroom": result[12], "buildyear": result[13],
                               "std_model": result[14], "builder": result[15], "widthboat_feet": result[16],
                               "bt_comment": result[17], "port": result[21], "port_id": result[22]}
                    json_data_rv.append(content_rv)
                data = {'sedna': json_data, 'mmk': json_data_mmk, 'nausys': json_data_nausys, 'data': json_data_rv}
                print(data)
                return jsonify(data)


        except Error as e:
            return (e)


    #@app.route('/api_get_boats/',  methods=['GET'])
    def api_get_boats(self):
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM boats LEFT JOIN boats_apis_sych ON boats_apis_sych.sedna_id = boats.boat_id;')
                rv_data = cursor.fetchall()
                json_data_rv = []
                for result in rv_data:
                    content_rv = {"name": result[1], "id": result[2], "mmkid": result[5], "nausys": result[6]}
                    json_data_rv.append(content_rv)
                cursor.execute('SELECT * FROM `api_mmk_sych` ORDER BY sych_id DESC LIMIT 5')
                mmk_log_data = cursor.fetchall()

                json_mmk_log_data = []
                for mmk_result in mmk_log_data:
                    mmk_content_rv = {
                        "id": mmk_result[0], "log":mmk_result[1], "date":mmk_result[3], "count":mmk_result[2]
                    }
                    json_mmk_log_data.append(mmk_content_rv)
                cursor.execute('SELECT * FROM `api_nausys_sych` ORDER BY `sych_id_n` DESC LIMIT 5')
                nausys_log_data = cursor.fetchall()
                json_nausys_log_data = []
                for nausys_result in nausys_log_data:
                    nausys_content_rv = {
                        "id": nausys_result[0], "log": nausys_result[1], "date": nausys_result[3], "count": nausys_result[2]
                    }
                    json_nausys_log_data.append(nausys_content_rv)


                data = {'data': json_data_rv, 'mmk_logs': json_mmk_log_data, 'nausys_logs': json_nausys_log_data }
                print(data)
                return jsonify(data)


        except Error as e:
            return (e)

    """ Send Sedna To MMK By Id Boat """

    #@app.route('/send_sedna_to_mmk_id/',  methods=['GET'])
    def send_sedna_to_mmk_id(self):
        boatid = request.args.get("boatid", None)
        print(boatid)
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM `boats_booking` LEFT JOIN `boats_apis_sych` ON `boats_booking`.`boat_id` = `boats_apis_sych`.`sedna_id` WHERE `book_id` =' +boatid)
                boats = cursor.fetchall()
                import requests
                import json
                url = "https://www.booking-manager.com/api/v2/reservation"
                print(boats)
                payload = json.dumps({
                    "dateFrom": boats[0][3].strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                    "dateTo": boats[0][4].strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
                    "yachtId": boats[0][8],
                    "status": 2
                })
                headers = {
                    'Authorization': 'Bearer 837-d6973f84d9b2752274d9695ee411b01176871329d36b12872601a0837b390374104b7fa3542e0aefade6f65835bd09885f372592ddc57b44a2a853602dd03cc2',
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)

                print(response.text)
                try:
                    json.loads(response.text)
                except ValueError as e:
                    return jsonify(response.text);
                mmk_result = json.loads(response.text)
                print(mmk_result["id"])
                url = "https://www.booking-manager.com/api/v2/reservation/" + str(mmk_result["id"])
                response = requests.request("PUT", url, headers=headers, data=payload)

                print(response.text)
                return jsonify('{Reservation Success}');

        except Error as e:
            return (e)


    #@app.route('/send_sedna_to_nausys_id/',  methods=['GET'])
    def send_sedna_to_nausys_id(self):
        boatid = request.args.get("boatid", None)
        print(boatid)
        try:
            conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                                 password='sd5w2V!0')
            if conn.is_connected():
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM `boats_booking` LEFT JOIN `boats_apis_sych` ON `boats_booking`.`boat_id` = `boats_apis_sych`.`sedna_id` WHERE `book_id` =' +boatid)
                boats = cursor.fetchall()
                import requests
                import json
                url = "http://ws.nausys.com/CBMS-external/rest/booking/v6/createInfo/"
                print(boats)
                payload = json.dumps({
                    "client": {
                        "name": "Rest",
                        "surname": "client",
                        "company": "false",
                        "vatNr": "",
                        "address": "address",
                        "zip": "",
                        "city": "",
                        "countryId": "100116",
                        "email": "somebody@someone.some",
                        "phone": "",
                        "mobile": "",
                        "skype": ""
                    },
                    "credentials": {
                        "username": "rest@FLY",
                        "password": "restFyly761"
                    },
                    "periodFrom": boats[0][3].strftime('%d.%m.%Y'),
                    "periodTo": boats[0][4].strftime('%d.%m.%Y'),
                    "yachtID":  boats[0][9],
                })

                headers = {
                    'Content-Type': 'application/json'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                print(json.loads(response.text)['uuid'])
                print(json.loads(response.text)['id'])

                if 'id' in json.loads(response.text):

                    url = "http://ws.nausys.com/CBMS-external/rest/booking/v6/createBooking"

                    payload = json.dumps({
                        "credentials": {
                            "username": "rest@FLY",
                            "password": "restFyly761"
                        },
                        "id": json.loads(response.text)['id'],
                        "uuid": json.loads(response.text)['uuid']

                    })
                    headers = {
                        'Content-Type': 'application/json'
                    }

                    responses = requests.request("POST", url, headers=headers, data=payload)



                    return jsonify(responses.text);

                else:
                    return jsonify("{error:error}")




        except Error as e:
            return (e)

    """ MMK DELETE By Id Boat """

    #@app.route('/delete_mmk_id/',  methods=['GET'])
    def delete_mmk_id(self):
        boatid = request.args.get("boatid", None)
        print(boatid)
        import requests
        import json
        payload =""
        headers = {
            'Authorization': 'Bearer 837-d6973f84d9b2752274d9695ee411b01176871329d36b12872601a0837b390374104b7fa3542e0aefade6f65835bd09885f372592ddc57b44a2a853602dd03cc2',
            'Content-Type': 'application/json'
        }
        url = "https://www.booking-manager.com/api/v2/reservation/" + str(boatid)
        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text)
        return jsonify('{Reservation Delete}');



    #@app.route('/nausys_import_boats/',  methods=['GET'])
    def nausys_import_boats(self):

        boats_bookings =Nausys()
        boats = json.loads(boats_bookings.nausys_import_boats())
        return jsonify(boats)
