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
        cursor.execute('DROP TABLE IF EXISTS crew_boats;')
        cursor.execute('DROP TABLE IF EXISTS crew_boats_basic;')

        # cursor.execute('DROP TABLE IF EXISTS boats_booking;')
        cursor.execute('TRUNCATE TABLE crew_images_boats;')
        cursor.execute('TRUNCATE TABLE crew_amenties;')
        cursor.execute('TRUNCATE TABLE crew_water_sports;')
        cursor.execute('TRUNCATE TABLE crew_characteristics;')
        cursor.execute('TRUNCATE TABLE crew_video_boats;')
        cursor.execute('TRUNCATE TABLE crew_sample_menu;')
        print('Creating table....')
        # in the below line please pass the create table statement which you want #to create
        cursor.execute(
            "CREATE TABLE `user7313393746_booking`.`crew_boats` ( `id` INT NOT NULL AUTO_INCREMENT ,`boat_name` VARCHAR(255), `boat_category` VARCHAR(255), `boat_id` INT(11) NOT NULL , PRIMARY KEY (`id`))")
        print("Table crew_boats is created....")

        cursor.execute(
            "CREATE TABLE `user7313393746_booking`.`crew_boats_basic` (`id` INT NOT NULL AUTO_INCREMENT, `boat_id` INT(11) NOT NULL, `size` VARCHAR(255), `sizeft` VARCHAR(255), `yachtYearBuilt` VARCHAR(255), `yachtPax` INT(11), `yachtCabins` INT(11), `yachtCrew` INT(11), `yachtLowNumericPrice` FLOAT(11), `yachtHighNumericPrice` FLOAT(11), `yachtBuilder` VARCHAR(255), `yachtPrefPickup` VARCHAR(255), PRIMARY KEY (`id`))")
        print("Table crew_boats_basic  is created....")

        # cursor.execute(
        # "CREATE TABLE `user7313393746_booking`.`boats_booking` ( `book_id` INT NOT NULL AUTO_INCREMENT , `boat_id` INT(11) NOT NULL , `status` INT(11) NOT NULL , `datestart` VARCHAR(255) , `dateend` VARCHAR(255) , PRIMARY KEY (`book_id`))")
        # print("Table Boat Bookings is created....")






except Error as e:
    print(e)

import requests

reqUrl = "http://www.centralyachtagent.com/snapins/snyachts-xml.php?user=1318&apicode=1318FYLY7hSs%d49hjQ"
mycursor = conn.cursor()
mycursor.execute('SELECT * FROM crew_boats_select')
row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
rv = mycursor.fetchall()
for result in rv:
    print(result[1])
    reqUrl = "http://www.centralyachtagent.com/snapins/ebrochure-xml.php?user=1318&apicode=1318FYLY7hSs%d49hjQ&idin=" + str(
        result[1])

    payload = ""
    mycursor = conn.cursor()
    response = requests.request("GET", reqUrl, data=payload)
    import xml.etree.ElementTree as ET

    xml = ET.fromstring(response.text)

    for holiday in xml.findall('yacht'):
        print(len(holiday))
        if len(holiday) > 1:
            sql = "INSERT INTO crew_boats (boat_name, boat_id, boat_category) VALUES (%s, %s, %s)"
            print(holiday)
            val = (holiday[1].text, holiday[0].text, holiday[4].text)
            mycursor.execute(sql, val)

            conn.commit()

            sql_extra = "INSERT  INTO `crew_boats_basic` (`id`, `boat_id`, `size`, `sizeft`, `yachtYearBuilt`, `yachtPax`, `yachtCabins`, `yachtCrew`, `yachtLowNumericPrice`, `yachtHighNumericPrice`, `yachtBuilder`, `yachtPrefPickup`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val_extra = (
            holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text, holiday[13].text,
            holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text, holiday[28].text)
            mycursor.execute(sql_extra, val_extra)

            image_count = 181
            all_images = str(holiday[180].text)
            while (image_count < 199):

                if holiday[image_count].text:

                    all_images += "|" + holiday[image_count].text
                image_count = image_count + 1


            sql_images = "INSERT INTO `crew_images_boats` (`id`, `boat_id`, `image_crew`, `extra_images`) VALUES (NULL, %s, %s, %s);"
            val_images = (holiday[0].text, holiday[180].text, all_images)
            mycursor.execute(sql_images, val_images)

            sql_amenties = "INSERT INTO `crew_amenties`(`amenties_id`, `boat_id`, `yachtSalonStereo`, `yachtSatTv`, `yachtIpod`, `yachtSunAwning`,`yachtHammock`, `yachtWindScoops`, `yachtDeckShower`, `yachtBimini`, `yachtSpecialDiets`, `yachtKosher`, `yachtBBQ`, `yachtNumDineIn`, `yachtNudeCharters`, `yachtHairDryer`, `yachtNumHatch`, `yachtCrewSmoke`, `yachtGuestSmoke`, `yachtGuestPet`, `yachtChildrenAllowed`, `yachtGym`, `yachtElevators`, `yachtWheelChairAccess`, `yachtGenerator`, `yachtInverter`, `yachtWaterMaker`, `yachtIceMaker`, `yachtStabilizers`, `yachtInternet`, `yachtGreenMakeWater`, `yachtGreenReuseBottle`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)";
            val_amenties = (
            holiday[0].text, holiday[48].text, holiday[281].text, holiday[282].text, holiday[55].text, holiday[56].text,
            holiday[57].text, holiday[58].text, holiday[59].text, holiday[60].text, holiday[61].text, holiday[62].text,
            holiday[54].text, holiday[64].text, holiday[65].text, holiday[66].text, holiday[211].text, holiday[67].text,
            holiday[68].text, holiday[69].text, holiday[23].text, holiday[25].text, holiday[26].text, holiday[71].text,
            holiday[74].text, holiday[75].text, holiday[76].text, holiday[24].text, holiday[285].text, holiday[110].text,
            holiday[111].text)
            mycursor.execute(sql_amenties, val_amenties)

            sql_watersports = "INSERT INTO `crew_water_sports` (`id`, `boat_id`, `yachtDinghy`, `yachtDinghyHp`, `yachtDinghyPax`, `yachtAdultWSkis`, `yachtKidsSkis`, `yachtJetSkis`, `yachtWaveRun`, `yachtKneeBoard`, `yachtStandUpPaddle`, `yachtWindSurf`, `yachtGearSnorkel`, `yachtTube`, `yachtScurfer`, `yachtWakeBoard`, `yacht1ManKayak`, `yacht2ManKayak`, `yachtSeaBob`, `yachtSeaScooter`, `yachtKiteBoarding`, `yachtFishingGear`, `yachtFishGearType`, `yachtNumFishRods`, `yachtDeepSeaFish`, `yachtUnderWaterCam`, `yachtUnderWaterVideo`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val_watersports = (
            holiday[0].text, holiday[79].text, holiday[80].text, holiday[81].text, holiday[82].text, holiday[83].text,
            holiday[84].text, holiday[85].text, holiday[86].text, holiday[87].text, holiday[88].text, holiday[89].text,
            holiday[90].text, holiday[91].text, holiday[92].text, holiday[93].text, holiday[94].text, holiday[95].text,
            holiday[96].text, holiday[97].text, holiday[105].text, holiday[106].text, holiday[107].text, holiday[280].text,
            holiday[108].text, holiday[109].text)
            mycursor.execute(sql_watersports, val_watersports)

            sql_generic = "INSERT INTO `crew_characteristics` (`id`, `boat_id`, `yachtShowers`, `yachtTubs`, `yachtWashBasins`, `yachtHeads`, `yachtElectricHeads`, `yachtHelipad`, `yachtJacuzzi`, `yachtAc`, `yachtPrefPickup`, `yachtOtherPickup`, `yachtEngines`, `yachtFuel`, `yachtCruiseSpeed`, `yachtMaxSpeed`, `yachtAccommodations`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val_generic = (
            holiday[0].text, holiday[175].text, holiday[268].text, holiday[176].text, holiday[177].text, holiday[178].text,
            holiday[21].text, holiday[22].text, holiday[27].text, holiday[28].text, holiday[29].text,
            holiday[72].text, holiday[73].text, holiday[36].text, holiday[37].text, holiday[38].text)
            mycursor.execute(sql_generic, val_generic)

            sql_crew = "INSERT INTO `crew_boat_crewd` (`id`, `boat_id`, `crew_num`, `yachtCaptainName`, `yachtCaptainNation`, `yachtCaptainBorn`, `yachtCaptainLang`, `yachtCrewName`, `yachtCrewTitle`, `yachtCrewNation`, `yachtCrewYrBorn`, `yachtCrewProfile`, `yachtCrewPhoto`, `yachtCrew1Pic`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
            val_crew = (
            holiday[0].text, holiday[210].text, holiday[214].text, holiday[215].text, holiday[216].text, holiday[220].text,
            holiday[221].text, holiday[222].text, holiday[223].text, holiday[224].text, holiday[229].text,
            holiday[230].text, holiday[231].text)
            mycursor.execute(sql_crew, val_crew)

            video_sql = "INSERT INTO `crew_video_boats` (`boat_id`, `video_url`) VALUES (%s, %s);"
            video_val = (holiday[0].text, holiday[35].text)
            mycursor.execute(video_sql, video_val)

            menu_sql = "INSERT INTO `crew_sample_menu` (`boat_id`, `text_menu`) VALUES (%s, %s);"
            menu_val = (holiday[0].text, holiday[199].text)
            mycursor.execute(menu_sql, menu_val)


