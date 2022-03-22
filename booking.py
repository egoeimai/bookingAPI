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
        cursor.execute('DROP TABLE IF EXISTS boats;')
        cursor.execute('TRUNCATE TABLE boats_bases;')
        #cursor.execute('DROP TABLE IF EXISTS boats_booking;')
        #cursor.execute('TRUNCATE TABLE boat_characteristics;')
        #cursor.execute('TRUNCATE TABLE boat_prices;')
        #cursor.execute('TRUNCATE TABLE boats_extras;')
        print('Creating table....')
        # in the below line please pass the create table statement which you want #to create
        cursor.execute("CREATE TABLE `user7313393746_booking`.`boats` ( `id` INT NOT NULL AUTO_INCREMENT , `boat_name` VARCHAR(255) , `boat_id` INT(11) NOT NULL , PRIMARY KEY (`id`))")
        print("Table Boat is created....")

        #cursor.execute(
           # "CREATE TABLE `user7313393746_booking`.`boats_extras` (`id` INT NOT NULL AUTO_INCREMENT, `id_opt` INT(11) NOT NULL, `id_opt_bt` INT(11) NOT NULL, `name` VARCHAR(255), `price` FLOAT(11) NOT NULL , `per` VARCHAR(255), `boat_id` INT(11) NOT NULL, PRIMARY KEY (`id`))")
       # print("Table Boat EXTRAS is created....")

        #cursor.execute(
            #"CREATE TABLE `user7313393746_booking`.`boats_booking` ( `book_id` INT NOT NULL AUTO_INCREMENT , `boat_id` INT(11) NOT NULL , `status` INT(11) NOT NULL , `datestart` VARCHAR(255) , `dateend` VARCHAR(255) , PRIMARY KEY (`book_id`))")
        #print("Table Boat Bookings is created....")

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
response = requests.request("GET", reqUrl, data=payload,  headers=headersList)
import xml.etree.ElementTree as ET
xml=ET.fromstring(response.text)
for holiday in xml.findall('boat'):


    sql = "INSERT INTO boats (boat_name, boat_id) VALUES (%s, %s)"
    val = (holiday.attrib['name'], holiday.attrib['id_boat'])
    mycursor.execute(sql, val)

    conn.commit()

    print(mycursor.rowcount, "record inserted.")

    #sqls = "INSERT INTO `boat_characteristics` (`boat_id`, `bt_type`, `crew`, `model`, `widthboat`, `nbdoucabin`, `nbsimcabin`, `nbper`, `nbbathroom`, `buildyear`, `std_model`, `builder`, `widthboat_feet`, `bt_comment`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    #vals = (holiday.attrib['id_boat'], holiday.attrib['bt_type'], holiday.attrib['crew'], holiday.attrib['model'], holiday.attrib['widthboat'], holiday.attrib['nbdoucabin'], holiday.attrib['nbsimcabin'], holiday.attrib['nbper'], holiday.attrib['nbbathroom'], holiday.attrib['buildyear'], holiday.attrib['std_model'], holiday.attrib['builder'], holiday.attrib['widthboat_feet'], holiday.attrib['bt_comment'])
    #mycursor.execute(sqls, vals)

    print(holiday.iter('homeport'))
    homeports = holiday.findall('homeport')
    for homeport in homeports:

        sql_bases = "INSERT INTO boats_bases (boat_id, destination_id, destination_name) VALUES (%s, %s, %s)"
        val_bases = (holiday.attrib['id_boat'], homeport.attrib['id_base'], homeport.attrib['name'])
        mycursor.execute(sql_bases, val_bases)

    conn.commit()
    #conn.commit()

    #images = holiday.findall('picts')
    #print(type(images))
    #for pictures in images:
        #images_inner = pictures.findall('pict')
       # for pictures_inner in images_inner:
           # print(pictures_inner.attrib['link'])
            #sqls_images = "INSERT INTO `boat_images` (`boat_id`, `image_url`) VALUES (%s, %s);"
            #images_vals = (holiday.attrib['id_boat'], pictures_inner.attrib['link'])
            #mycursor.execute(sqls_images, images_vals)

            #conn.commit()
    #characteristics = holiday.findall('characteristics')
    #for characteristic_topic in characteristics:
        #characteristic = characteristic_topic.findall('characteristic_topic')
       # for characteristic_inner in characteristic:
          #  print(characteristic_inner.attrib['topic'])
           # for characteristic_list in characteristic_inner:
             #   print(characteristic_list.attrib['name'])

    #characteristics = holiday.findall('characteristics')
    #for characteristic_topic in characteristics:
        #characteristic = characteristic_topic.findall('characteristic_topic')
       # for characteristic_inner in characteristic:
          #  print(characteristic_inner.attrib['topic'])
           # for characteristic_list in characteristic_inner:
             #   print(characteristic_list.attrib['name'])

    prices = holiday.findall('prices')
    for price in prices:
        price_inner = price.findall('price')
        for price_val in price_inner:
            print(price_val.attrib['amount'])
            sqls_price = "INSERT INTO `boat_prices` (`boat_id`, `datestart`, `dateend`, `amount`, `unitamount`) VALUES (%s, %s, %s, %s, %s);"
            price_vals = (holiday.attrib['id_boat'], price_val.attrib['datestart'], price_val.attrib['dateend'], price_val.attrib['amount'], price_val.attrib['unitamount'])
            mycursor.execute(sqls_price, price_vals)




mycursor.execute('SELECT * FROM boats')
row_headers = [x[0] for x in mycursor.description] #this will extract row headers
rv = mycursor.fetchall()
for result in rv:

    extras_url = "https://api.sednasystem.com/API/getExtras3.asp?id_boat="+ str(result[2]) +"&refope=ysy171"

    payload_extras = ""
    response_extras = requests.request("GET", extras_url, data=payload_extras, headers=headersList)

    xml_extras = ET.fromstring(response_extras.text)

    for holiday_extras in xml_extras.findall('extra'):
        print(result[2])
        #sql_extras = "INSERT INTO `boats_extras` (`id_opt`, `id_opt_bt`, `name`, `price`, `per`, `boat_id`) VALUES (%s, %s, %s, %s, %s, %s);"
        #val_extras = (holiday_extras.attrib['id_opt'], holiday_extras.attrib['id_opt_bt'], holiday_extras.attrib['name'], holiday_extras.attrib['price'], holiday_extras.attrib['per'], result[2])
        #mycursor.execute(sql_extras, val_extras)

        conn.commit()

    reqUrl = "https://api.sednasystem.com/api/getBookingData.asp?api_mode=xml&appname=apiboatcharter&token=" + token + "&id_boat=" + str(result[2]) + "&date_start=2021-01-01&date_end=2022-12-31"
    payload_bo = ""
    response_bo = requests.request("GET", reqUrl, data=payload_bo, headers=headersList)

    xml_bo = ET.fromstring(response_bo.text)
    for holiday_bo in xml_bo.findall('charter'):
        #sql = "INSERT INTO boats_booking (boat_id, status, datestart, dateend) VALUES (%s, %s, %s, %s)"
        #val = (result[2], holiday_bo.attrib['status'], holiday_bo.attrib['datestart'], holiday_bo.attrib['dateend'])
       # mycursor.execute(sql, val)

        conn.commit()