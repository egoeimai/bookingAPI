import requests
import mysql.connector as mysql
from mysql.connector import Error

token = ""
try:
    conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                         password='sd5w2V!0')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('TRUNCATE TABLE crew_boats_reviews;')




except Error as e:

    print(e)

import requests

mycursor = conn.cursor()
mycursor.execute('SELECT * FROM crew_boats_select')
row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
rv = mycursor.fetchall()
for result in rv:
    print(result[1])

    reqUrl = "http://www.centralyachtagent.com/snapins/guestcomments-xml.php?user=1318&idin=" + str(
        result[1]) + "&act=website&apicode=1318FYLY7hSs%d49hjQ"

    payload = ""
    mycursor = conn.cursor()
    response = requests.request("GET", reqUrl, data=payload)
    import xml.etree.ElementTree as ET

    xml = ET.fromstring(response.text)

    for holiday in xml.findall('yacht'):
        print(len(holiday))

        if len(holiday) > 1:
            sql = "INSERT INTO `crew_boats_reviews` (`review_id`, `boat_id`, `review_url1`, `review_url2`, `review_url3`) VALUES (NULL, %s, %s, %s, %s);"
            val = (result[1], holiday[2].text, holiday[3].text, holiday[4].text)
            mycursor.execute(sql, val)

            conn.commit()