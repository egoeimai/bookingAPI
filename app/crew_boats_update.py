import requests
import mysql.connector as mysql
from mysql.connector import Error
import hashlib


def crew_update():

    token = ""
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            #cursor.execute('DROP TABLE IF EXISTS crew_boats;')
            #cursor.execute('DROP TABLE IF EXISTS crew_boats_basic;')

            # cursor.execute('DROP TABLE IF EXISTS boats_booking;')
            #cursor.execute('TRUNCATE TABLE crew_images_boats;')
            #cursor.execute('TRUNCATE TABLE crew_boat_crewd;')
            #cursor.execute('TRUNCATE TABLE crew_amenties;')
            #cursor.execute('TRUNCATE TABLE crew_water_sports;')
            #cursor.execute('TRUNCATE TABLE crew_characteristics;')
            #cursor.execute('TRUNCATE TABLE crew_video_boats;')
            #cursor.execute('TRUNCATE TABLE crew_yachtothertoys;')
            #cursor.execute('TRUNCATE TABLE crew_yachtotherentertain;')
            #cursor.execute('TRUNCATE TABLE crew_sample_menu;')
            print('Creating table....')
            # in the below line please pass the create table statement which you want #to create
            #cursor.execute("CREATE TABLE `user7313393746_booking`.`crew_boats` ( `id` INT NOT NULL AUTO_INCREMENT ,`boat_name` VARCHAR(255), `boat_category` VARCHAR(255), `boat_id` INT(11) NOT NULL , PRIMARY KEY (`id`))")
            print("Table crew_boats is created....")

            #cursor.execute("CREATE TABLE `user7313393746_booking`.`crew_boats_basic` (`id` INT NOT NULL AUTO_INCREMENT, `boat_id` INT(11) NOT NULL, `size` VARCHAR(255), `sizeft` VARCHAR(255), `yachtYearBuilt` VARCHAR(255), `yachtPax` INT(11), `yachtCabins` INT(11), `yachtCrew` INT(11), `yachtLowNumericPrice` FLOAT(11), `yachtHighNumericPrice` FLOAT(11), `yachtBuilder` VARCHAR(255), `yachtPrefPickup` VARCHAR(255), `yacht_description` LONGTEXT, `price_details` LONGTEXT, `location_details` LONGTEXT, `broker_notes` LONGTEXT, `hash` VARCHAR(255),  PRIMARY KEY (`id`))")
            print("Table crew_boats_basic  is created....")

            # cursor.execute(
            # "CREATE TABLE `user7313393746_booking`.`boats_booking` ( `book_id` INT NOT NULL AUTO_INCREMENT , `boat_id` INT(11) NOT NULL , `status` INT(11) NOT NULL , `datestart` VARCHAR(255) , `dateend` VARCHAR(255) , PRIMARY KEY (`book_id`))")
            # print("Table Boat Bookings is created....")






    except Error as e:
        print(e)

    import requests

    reqUrl = "http://www.centralyachtagent.com/snapins/snyachts-xml.php?user=1318&apicode=1318FYLY7hSs%d49hjQ"
    mycursor = conn.cursor()
    mycursor.execute('SELECT * FROM crew_boats_select WHERE is_fyly = 1')
    row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
    rv = mycursor.fetchall()
    Boat_log = ""
    for result in rv:
       # print(result[1])
        reqUrl = "http://www.centralyachtagent.com/snapins/ebrochure-xml.php?user=1318&apicode=1318FYLY7hSs%d49hjQ&idin=" + str(
            result[1])

        payload = ""
        mycursor = conn.cursor()
        response = requests.request("GET", reqUrl, data=payload)
        import xml.etree.ElementTree as ET
        try:
            parser = ET.XMLParser(encoding="utf-8")
            xml = ET.fromstring(response.text, parser=parser)

            for holiday in xml.findall('yacht'):

                #print(len(holiday))
                if len(holiday) > 1:


                    mycursor.execute("SELECT boat_id, hash, id FROM crew_boats_basic WHERE boat_id=" + holiday[0].text);
                    boat_exist = mycursor.fetchall();
                    if (len(boat_exist) == 0):

                        sql = "INSERT INTO crew_boats (boat_name, boat_id, boat_category) VALUES (%s, %s, %s)"
                        print(holiday)
                        val = (holiday[1].text, holiday[0].text, holiday[4].text)
                        mycursor.execute(sql, val)

                        conn.commit();

                        crew_boats_basic_hash = (holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text, holiday[13].text,
                        holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text, holiday[28].text, holiday[130].text, holiday[269].text, holiday[271].text, holiday[284].text,  holiday[20].text)


                        sql_extra = "INSERT  INTO `crew_boats_basic` (`id`, `boat_id`, `size`, `sizeft`, `yachtYearBuilt`, `yachtPax`, `yachtCabins`, `yachtCrew`, `yachtLowNumericPrice`, `yachtHighNumericPrice`, `yachtBuilder`, `yachtPrefPickup`, `yacht_description`, `price_details`, `location_details`, `broker_notes`,  `yachtRefit`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val_extra = (holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text, holiday[13].text,
                        holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text, holiday[28].text, holiday[130].text, holiday[269].text, holiday[271].text, holiday[284].text, holiday[20].text, hashlib.md5(str(crew_boats_basic_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_extra, val_extra)

                        image_count = 181
                        all_images = str(holiday[180].text)
                        while (image_count < 199):

                            if holiday[image_count].text:

                                all_images += "|" + holiday[image_count].text
                            image_count = image_count + 1

                        #Insert Images of Boat
                        val_images_hash = (holiday[0].text, holiday[180].text, all_images)
                        sql_images = "INSERT INTO `crew_images_boats` (`id`, `boat_id`, `image_crew`, `extra_images`, `hash`) VALUES (NULL, %s, %s, %s, %s);"
                        val_images = (holiday[0].text, holiday[180].text, all_images, hashlib.md5(str(val_images_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_images, val_images)


                        #Insert Entertaiment of Boat

                        val_yachtotherentertain_hash = (holiday[0].text, holiday[171].text)

                        sql_yachtotherentertain = "INSERT INTO `crew_yachtotherentertain` (`other_id`, `boat_id`, `yachtotherentertain`, `hash`) VALUES (NULL, %s, %s, %s);"
                        val_yachtotherentertain = (holiday[0].text, holiday[171].text, hashlib.md5(str(val_yachtotherentertain_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_yachtotherentertain, val_yachtotherentertain)

                        # Insert Other Toys  of Boat
                        val_othertoys_hash = (holiday[0].text, holiday[170].text)
                        sql_othertoys = "INSERT INTO `crew_yachtothertoys` (`id_other`, `boat_id`, `yachtothertoys`, `hash`) VALUES (NULL, %s, %s, %s);"
                        val_othertoys = (holiday[0].text, holiday[170].text, hashlib.md5(str(val_othertoys_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_othertoys, val_othertoys)

                        # Insert Amenities

                        val_amenties_hash = (
                        holiday[0].text, holiday[48].text, holiday[281].text, holiday[282].text, holiday[55].text, holiday[56].text,
                        holiday[57].text, holiday[58].text, holiday[59].text, holiday[60].text, holiday[61].text, holiday[62].text,
                        holiday[54].text, holiday[64].text, holiday[65].text, holiday[66].text, holiday[211].text, holiday[67].text,
                        holiday[68].text, holiday[69].text, holiday[23].text, holiday[25].text, holiday[26].text, holiday[71].text,
                        holiday[74].text, holiday[75].text, holiday[76].text, holiday[24].text, holiday[285].text, holiday[110].text,
                        holiday[111].text)
                        sql_amenties = "INSERT INTO `crew_amenties`(`amenties_id`, `boat_id`, `yachtSalonStereo`, `yachtSatTv`, `yachtIpod`, `yachtSunAwning`,`yachtHammock`, `yachtWindScoops`, `yachtDeckShower`, `yachtBimini`, `yachtSpecialDiets`, `yachtKosher`, `yachtBBQ`, `yachtNumDineIn`, `yachtNudeCharters`, `yachtHairDryer`, `yachtNumHatch`, `yachtCrewSmoke`, `yachtGuestSmoke`, `yachtGuestPet`, `yachtChildrenAllowed`, `yachtGym`, `yachtElevators`, `yachtWheelChairAccess`, `yachtGenerator`, `yachtInverter`, `yachtWaterMaker`, `yachtIceMaker`, `yachtStabilizers`, `yachtInternet`, `yachtGreenMakeWater`, `yachtGreenReuseBottle`, `hash`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)";
                        val_amenties = (
                        holiday[0].text, holiday[48].text, holiday[281].text, holiday[282].text, holiday[55].text, holiday[56].text,
                        holiday[57].text, holiday[58].text, holiday[59].text, holiday[60].text, holiday[61].text, holiday[62].text,
                        holiday[54].text, holiday[64].text, holiday[65].text, holiday[66].text, holiday[211].text, holiday[67].text,
                        holiday[68].text, holiday[69].text, holiday[23].text, holiday[25].text, holiday[26].text, holiday[71].text,
                        holiday[74].text, holiday[75].text, holiday[76].text, holiday[24].text, holiday[285].text, holiday[110].text,
                        holiday[111].text, hashlib.md5(str(val_amenties_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_amenties, val_amenties)



                        # Insert WaterSports of Crew Boats

                        val_watersports_hash = (
                        holiday[0].text, holiday[79].text, holiday[80].text, holiday[81].text, holiday[82].text, holiday[83].text,
                        holiday[84].text, holiday[85].text, holiday[86].text, holiday[87].text, holiday[88].text, holiday[89].text,
                        holiday[90].text, holiday[91].text, holiday[92].text, holiday[93].text, holiday[94].text, holiday[95].text,
                        holiday[96].text, holiday[97].text, holiday[105].text, holiday[106].text, holiday[107].text, holiday[280].text,
                        holiday[108].text, holiday[109].text)

                        sql_watersports = "INSERT INTO `crew_water_sports` (`id`, `boat_id`, `yachtDinghy`, `yachtDinghyHp`, `yachtDinghyPax`, `yachtAdultWSkis`, `yachtKidsSkis`, `yachtJetSkis`, `yachtWaveRun`, `yachtKneeBoard`, `yachtStandUpPaddle`, `yachtWindSurf`, `yachtGearSnorkel`, `yachtTube`, `yachtScurfer`, `yachtWakeBoard`, `yacht1ManKayak`, `yacht2ManKayak`, `yachtSeaBob`, `yachtSeaScooter`, `yachtKiteBoarding`, `yachtFishingGear`, `yachtFishGearType`, `yachtNumFishRods`, `yachtDeepSeaFish`, `yachtUnderWaterCam`, `yachtUnderWaterVideo`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        val_watersports = (
                        holiday[0].text, holiday[79].text, holiday[80].text, holiday[81].text, holiday[82].text, holiday[83].text,
                        holiday[84].text, holiday[85].text, holiday[86].text, holiday[87].text, holiday[88].text, holiday[89].text,
                        holiday[90].text, holiday[91].text, holiday[92].text, holiday[93].text, holiday[94].text, holiday[95].text,
                        holiday[96].text, holiday[97].text, holiday[105].text, holiday[106].text, holiday[107].text, holiday[280].text,
                        holiday[108].text, holiday[109].text, hashlib.md5(str(val_watersports_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_watersports, val_watersports)


                        # Insert Characteristics of Crew Boats

                        val_generic_hash = (
                        holiday[0].text, holiday[175].text, holiday[268].text, holiday[176].text, holiday[177].text, holiday[178].text,
                        holiday[21].text, holiday[22].text, holiday[27].text, holiday[28].text, holiday[29].text,
                        holiday[72].text, holiday[73].text, holiday[36].text, holiday[37].text, holiday[38].text)

                        sql_generic = "INSERT INTO `crew_characteristics` (`id`, `boat_id`, `yachtShowers`, `yachtTubs`, `yachtWashBasins`, `yachtHeads`, `yachtElectricHeads`, `yachtHelipad`, `yachtJacuzzi`, `yachtAc`, `yachtPrefPickup`, `yachtOtherPickup`, `yachtEngines`, `yachtFuel`, `yachtCruiseSpeed`, `yachtMaxSpeed`, `yachtAccommodations`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        val_generic = (
                        holiday[0].text, holiday[175].text, holiday[268].text, holiday[176].text, holiday[177].text, holiday[178].text,
                        holiday[21].text, holiday[22].text, holiday[27].text, holiday[28].text, holiday[29].text,
                        holiday[72].text, holiday[73].text, holiday[36].text, holiday[37].text, holiday[38].text, hashlib.md5(str(val_generic_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_generic, val_generic)

                        # Insert Crew Crewed
                        val_crew_hash = (
                        holiday[0].text, holiday[210].text, holiday[214].text, holiday[215].text, holiday[216].text, holiday[220].text,
                        holiday[221].text, holiday[222].text, holiday[223].text, holiday[224].text, holiday[229].text,
                        holiday[230].text, holiday[231].text, holiday[232].text, holiday[233].text,
                            holiday[234].text, holiday[235].text, holiday[236].text, holiday[237].text,
                            holiday[238].text, holiday[239].text, holiday[240].text)

                        sql_crew = "INSERT INTO `crew_boat_crewd` (`id`, `boat_id`, `crew_num`, `yachtCaptainName`, `yachtCaptainNation`, `yachtCaptainBorn`, `yachtCaptainLang`, `yachtCrewName`, `yachtCrewTitle`, `yachtCrewNation`, `yachtCrewYrBorn`, `yachtCrewProfile`, `yachtCrewPhoto`, `yachtCrew1Pic`, `yachtCrew2Pic`, `yachtCrew3Pic`, `yachtCrew4Pic`, `yachtCrew5Pic`, `yachtCrew6Pic`, `yachtCrew7Pic`, `yachtCrew8Pic`, `yachtCrew9Pic`, `yachtCrew10Pic`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        val_crew = (
                            holiday[0].text, holiday[210].text, holiday[214].text, holiday[215].text,
                            holiday[216].text, holiday[220].text,
                            holiday[221].text, holiday[222].text, holiday[223].text, holiday[224].text,
                            holiday[229].text,
                            holiday[230].text, holiday[231].text, holiday[232].text, holiday[233].text,
                            holiday[234].text, holiday[235].text, holiday[236].text, holiday[237].text,
                            holiday[238].text, holiday[239].text, holiday[240].text,
                            hashlib.md5(str(val_crew_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_crew, val_crew)

                        # Insert Videos of Crew
                        video_val_hash = (holiday[0].text, holiday[35].text)
                        video_sql = "INSERT INTO `crew_video_boats` (`boat_id`, `video_url`, `hash`) VALUES (%s, %s, %s);"
                        video_val = (holiday[0].text, holiday[35].text, hashlib.md5(str(video_val_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(video_sql, video_val)


                        # Insert Menu of Crew
                        menu_val_hash = (holiday[0].text, holiday[199].text, holiday[200].text, holiday[201].text, holiday[202].text, holiday[203].text, holiday[204].text, holiday[205].text, holiday[206].text, holiday[207].text, holiday[208].text, holiday[209].text)
                        menu_sql = "INSERT INTO `crew_sample_menu` (`boat_id`, `text_menu`, `hash`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        menu_val = (holiday[0].text, holiday[199].text, holiday[200].text, holiday[201].text, holiday[202].text, holiday[203].text, holiday[204].text, holiday[205].text, holiday[206].text, holiday[207].text, holiday[208].text, holiday[209].text, hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(menu_sql, menu_val)

                        val_boat_destinations_hash = (holiday[9].text, holiday[172].text, holiday[10].text)
                        val_boat_destinations_sql = "INSERT INTO `crewed_areas` (`boat_id`, `yachtPrefPickup`, `yachtSummerArea`, `yachtOtherPickup`, `hash`) VALUES (%s, %s, %s, %s, %s);"
                        val_boat_destinations_val = (holiday[0].text, holiday[28].text, holiday[173].text, holiday[29].text,
                                hashlib.md5(str(val_boat_destinations_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(val_boat_destinations_sql, val_boat_destinations_val)

                        conn.commit()

                    else:
                        #print(str(holiday.text))
                        print(boat_exist[0][0])

                        print(holiday[1].text)
                        Boat_log = Boat_log + "<h3>" + holiday[1].text + "</h3></br>";
                        crew_boats_basic_hash = (
                        holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text, holiday[13].text,
                        holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text, holiday[28].text,
                        holiday[130].text, holiday[269].text, holiday[271].text, holiday[286].text,  holiday[20].text)

                        print(hashlib.md5(str(crew_boats_basic_hash).encode("utf-8")).hexdigest())
                        if hashlib.md5(str(crew_boats_basic_hash).encode("utf-8")).hexdigest() == boat_exist[0][1]:
                            print("Δεν Αλλαξε Κατι Specs")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι Specs</br>"
                        else:
                            print("Αλλαξε Κατι Specs")
                            Boat_log = Boat_log + "Αλλαξε Κατι Specs</br>"
                            mycursor.execute("DELETE FROM crew_boats_basic WHERE id = " + str(int(boat_exist[0][2])))
                            boat_exist = mycursor.fetchall();
                            crew_boats_basic_hash = (
                            holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text,
                            holiday[13].text,
                            holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text, holiday[28].text,
                            holiday[130].text, holiday[269].text, holiday[271].text, holiday[286].text,  holiday[20].text)

                            sql_extra = "INSERT  INTO `crew_boats_basic` (`id`, `boat_id`, `size`, `sizeft`, `yachtYearBuilt`, `yachtPax`, `yachtCabins`, `yachtCrew`, `yachtLowNumericPrice`, `yachtHighNumericPrice`, `yachtBuilder`, `yachtPrefPickup`, `yacht_description`, `price_details`, `location_details`, `broker_notes`, `yachtRefit`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            val_extra = (holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text,
                                         holiday[13].text,
                                         holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text,
                                         holiday[28].text, holiday[130].text, holiday[269].text, holiday[271].text,
                                         holiday[286].text, holiday[20].text, hashlib.md5(str(crew_boats_basic_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_extra, val_extra)
                            conn.commit()

                        #Check Images of Boat
                        mycursor.execute("SELECT boat_id, hash, id FROM crew_images_boats WHERE boat_id=" + holiday[0].text);
                        boat_images_exist = mycursor.fetchall();
                        image_count = 181
                        all_images = str(holiday[180].text)
                        while (image_count < 199):

                            if holiday[image_count].text:
                                all_images += "|" + holiday[image_count].text
                            image_count = image_count + 1



                        # Insert Images of Boat
                        val_images_hash = (holiday[0].text, holiday[180].text, all_images)
                        if hashlib.md5(str(val_images_hash).encode("utf-8")).hexdigest() == boat_images_exist[0][1]:
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Φωτογραφίες</br>"
                            print("Δεν Αλλαξε Κατι από Φωτογραφίες")
                        else:
                            print("Αλλαξε Κατι από Φωτογραφίες")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Φωτογραφίες</br>"
                            mycursor.execute("DELETE FROM crew_images_boats WHERE id = " + str(int(boat_images_exist[0][2])))
                            boat_images_exist = mycursor.fetchall();
                            sql_images = "INSERT INTO `crew_images_boats` (`id`, `boat_id`, `image_crew`, `extra_images`, `hash`) VALUES (NULL, %s, %s, %s, %s);"
                            val_images = (holiday[0].text, holiday[180].text, all_images,
                                          hashlib.md5(str(val_images_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_images, val_images)

                        #Check Entertaiment of Boat
                        mycursor.execute("SELECT boat_id, hash, other_id FROM crew_yachtotherentertain WHERE boat_id=" + holiday[0].text);
                        boat_entertain_exist = mycursor.fetchall();

                        val_yachtotherentertain_hash = (holiday[0].text, holiday[171].text)

                        if hashlib.md5(str(val_yachtotherentertain_hash).encode("utf-8")).hexdigest() == boat_entertain_exist[0][1]:
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Entertain</br>"
                            print("Δεν Αλλαξε Κατι από Entertain")
                        else:
                            print("Αλλαξε Κατι από Entertain")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Entertain</br>"
                            mycursor.execute("DELETE FROM crew_yachtotherentertain WHERE other_id = " + str(int(boat_entertain_exist[0][2])))
                            boat_entertain_exist = mycursor.fetchall();
                            sql_yachtotherentertain = "INSERT INTO `crew_yachtotherentertain` (`other_id`, `boat_id`, `yachtotherentertain`, `hash`) VALUES (NULL, %s, %s, %s);"
                            val_yachtotherentertain = (holiday[0].text, holiday[171].text,
                                                       hashlib.md5(str(val_yachtotherentertain_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_yachtotherentertain, val_yachtotherentertain)

                        # Check Other Toys of Boat
                        mycursor.execute(
                            "SELECT boat_id, hash, id_other FROM crew_yachtothertoys WHERE boat_id=" + holiday[0].text);
                        boat_othertoys_exist = mycursor.fetchall();
                        val_othertoys_hash = (holiday[0].text, holiday[170].text)
                        # Insert Other Toys  of Boat
                        if hashlib.md5(str(val_othertoys_hash).encode("utf-8")).hexdigest() == boat_othertoys_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από Other Toys")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Other Toys</br>"
                        else:
                            print("Αλλαξε Κατι από Other Toys")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Other Toys</br>"
                            mycursor.execute("DELETE FROM crew_yachtothertoys WHERE id_other = " + str(int(boat_othertoys_exist[0][2])))
                            boat_othertoys_exist = mycursor.fetchall();
                            sql_othertoys = "INSERT INTO `crew_yachtothertoys` (`id_other`, `boat_id`, `yachtothertoys`, `hash`) VALUES (NULL, %s, %s, %s);"
                            val_othertoys = (
                            holiday[0].text, holiday[170].text, hashlib.md5(str(val_othertoys_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_othertoys, val_othertoys)

                            # Insert Amenities

                        mycursor.execute(
                            "SELECT boat_id, hash, amenties_id FROM crew_amenties WHERE boat_id=" + holiday[0].text);
                        boat_amenties_exist = mycursor.fetchall();


                        if  holiday[48].text:
                            yachtSalonStereo = holiday[48].text
                        else:
                            yachtSalonStereo = "<div class='nul'></div>"


                        if  holiday[281].text:
                            yachtSatTv = holiday[281].text
                        else:
                            yachtSatTv = "<div class='nul'></div>"

                        if  holiday[282].text:
                            yachtIpod = holiday[282].text
                        else:
                            yachtIpod = "<div class='nul'></div>"

                        if  holiday[55].text:
                            yachtSunAwning = holiday[55].text
                        else:
                            yachtSunAwning = "<div class='nul'></div>"

                        if  holiday[56].text:
                            yachtHammock = holiday[56].text
                        else:
                            yachtHammock = "<div class='nul'></div>"

                        if  holiday[57].text:
                            yachtWindScoops = holiday[57].text
                        else:
                            yachtWindScoops = "<div class='nul'></div>"


                        if  holiday[58].text:
                            yachtDeckShower = holiday[58].text
                        else:
                            yachtDeckShower = "<div class='nul'></div>"

                        if  holiday[59].text:
                            yachtBimini = holiday[59].text
                        else:
                            yachtBimini = "<div class='nul'></div>"

                        if  holiday[60].text:
                            yachtSpecialDiets = holiday[60].text
                        else:
                            yachtSpecialDiets = "<div class='nul'></div>"

                        if  holiday[61].text:
                            yachtKosher = holiday[61].text
                        else:
                            yachtKosher = "<div class='nul'></div>"

                        if  holiday[62].text:
                            yachtBBQ = holiday[62].text
                        else:
                            yachtBBQ = "<div class='nul'></div>"


                        if  holiday[54].text:
                            yachtNumDineIn = holiday[54].text
                        else:
                            yachtNumDineIn = "<div class='nul'></div>"

                        if holiday[64].text:
                            yachtNudeCharters = holiday[64].text
                        else:
                            yachtNudeCharters = "<div class='nul'></div>"


                        if holiday[65].text:
                            yachtHairDryer = holiday[65].text
                        else:
                            yachtHairDryer = "<div class='nul'></div>"

                        if holiday[66].text:
                            yachtNumHatch = holiday[66].text
                        else:
                            yachtNumHatch = "<div class='nul'></div>"

                        if holiday[211].text:
                            yachtCrewSmoke = holiday[211].text
                        else:
                            yachtCrewSmoke = "<div class='nul'></div>"

                        if holiday[67].text:
                            yachtGuestSmoke = holiday[67].text
                        else:
                            yachtGuestSmoke = "<div class='nul'></div>"

                        if holiday[68].text:
                            yachtGuestPet = holiday[68].text
                        else:
                            yachtGuestPet = "<div class='nul'></div>"


                        if holiday[69].text:
                            yachtChildrenAllowed = holiday[69].text
                        else:
                            yachtChildrenAllowed = "<div class='nul'></div>"

                        if holiday[23].text:
                            yachtGym = holiday[23].text
                        else:
                            yachtGym = "<div class='nul'></div>"

                        if holiday[25].text:
                            yachtElevators = holiday[25].text
                        else:
                            yachtElevators = "<div class='nul'></div>"

                        if holiday[26].text:
                            yachtWheelChairAccess = holiday[26].text
                        else:
                            yachtWheelChairAccess = "<div class='nul'></div>"



                        if holiday[71].text:
                            yachtGenerator = holiday[71].text
                        else:
                            yachtGenerator = "<div class='nul'></div>"


                        if holiday[74].text:
                            yachtInverter = holiday[74].text
                        else:
                            yachtInverter = "<div class='nul'></div>"


                        if holiday[75].text:
                            yachtWaterMaker = holiday[75].text
                        else:
                            yachtWaterMaker = "<div class='nul'></div>"


                        if holiday[76].text:
                            yachtIceMaker = holiday[76].text
                        else:
                            yachtIceMaker = "<div class='nul'></div>"


                        if holiday[24].text:
                            yachtStabilizers = holiday[24].text
                        else:
                            yachtStabilizers = "<div class='nul'></div>"


                        if holiday[285].text:
                            yachtInternet = holiday[285].text
                        else:
                            yachtInternet = "<div class='nul'></div>"



                        if holiday[110].text:
                            yachtGreenMakeWater = holiday[110].text
                        else:
                            yachtGreenMakeWater = "<div class='nul'></div>"


                        if holiday[110].text:
                            yachtGreenReuseBottle = holiday[110].text
                        else:
                            yachtGreenReuseBottle = "<div class='nul'></div>"


                        val_amenties_hash = (
                            holiday[0].text, yachtSalonStereo, yachtSatTv, yachtIpod, yachtSunAwning,
                            yachtHammock,
                            yachtWindScoops, yachtDeckShower, yachtBimini, yachtSpecialDiets, yachtKosher,
                            yachtBBQ,
                            yachtNumDineIn, yachtNudeCharters, yachtHairDryer, yachtNumHatch, yachtCrewSmoke,
                            yachtGuestSmoke,
                            yachtGuestPet, yachtChildrenAllowed, yachtGym, yachtElevators, yachtWheelChairAccess,
                            yachtGenerator,
                            yachtInverter, yachtWaterMaker, yachtIceMaker, yachtStabilizers, yachtInternet,
                            yachtGreenMakeWater,
                            yachtGreenReuseBottle)

                        if hashlib.md5(str(val_amenties_hash).encode("utf-8")).hexdigest() == boat_amenties_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από amenties")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από amenties</br>"
                        else:
                            print("Αλλαξε Κατι από amenties")
                            Boat_log = Boat_log + "Αλλαξε Κατι από amenties</br>"
                            mycursor.execute("DELETE FROM crew_amenties WHERE amenties_id = " + str(int(boat_amenties_exist[0][2])))
                            boat_amenties_exist = mycursor.fetchall();
                            sql_amenties = "INSERT INTO `crew_amenties`(`amenties_id`, `boat_id`, `yachtSalonStereo`, `yachtSatTv`, `yachtIpod`, `yachtSunAwning`,`yachtHammock`, `yachtWindScoops`, `yachtDeckShower`, `yachtBimini`, `yachtSpecialDiets`, `yachtKosher`, `yachtBBQ`, `yachtNumDineIn`, `yachtNudeCharters`, `yachtHairDryer`, `yachtNumHatch`, `yachtCrewSmoke`, `yachtGuestSmoke`, `yachtGuestPet`, `yachtChildrenAllowed`, `yachtGym`, `yachtElevators`, `yachtWheelChairAccess`, `yachtGenerator`, `yachtInverter`, `yachtWaterMaker`, `yachtIceMaker`, `yachtStabilizers`, `yachtInternet`, `yachtGreenMakeWater`, `yachtGreenReuseBottle`, `hash`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)";
                            val_amenties = (
                                holiday[0].text, yachtSalonStereo, yachtSatTv, yachtIpod, yachtSunAwning,
                                yachtHammock,
                                yachtWindScoops, yachtDeckShower, yachtBimini, yachtSpecialDiets, yachtKosher,
                                yachtBBQ,
                                yachtNumDineIn, yachtNudeCharters, yachtHairDryer, yachtNumHatch, yachtCrewSmoke,
                                yachtGuestSmoke,
                                yachtGuestPet, yachtChildrenAllowed, yachtGym, yachtElevators, yachtWheelChairAccess,
                                yachtGenerator,
                                yachtInverter, yachtWaterMaker, yachtIceMaker, yachtStabilizers, yachtInternet,
                                yachtGreenMakeWater,
                                yachtGreenReuseBottle, hashlib.md5(str(val_amenties_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_amenties, val_amenties)

                        # Check WaterSports of Crew Boats
                        mycursor.execute(
                            "SELECT boat_id, hash, id FROM crew_water_sports WHERE boat_id=" + holiday[0].text);
                        boat_watersports_exist = mycursor.fetchall();


                        if  holiday[109].text:
                            yachtUnderWaterVideo = holiday[109].text
                        else:
                            yachtUnderWaterVideo = "<div class='nul'></div>"

                        if  holiday[108].text:
                            yachtUnderWaterCam = holiday[108].text
                        else:
                            yachtUnderWaterCam = "<div class='nul'></div>"

                        if holiday[280].text:
                            yachtDeepSeaFish = holiday[280].text
                        else:
                            yachtDeepSeaFish = "<div class='nul'></div>"

                        if holiday[107].text:
                            yachtNumFishRods = holiday[107].text
                        else:
                            yachtNumFishRods = "<div class='nul'></div>"

                        if holiday[106].text :
                            yachtFishGearType = holiday[106].text
                        else:
                            yachtFishGearType = "<div class='nul'></div>"

                        if holiday[105].text:
                            yachtFishingGear = holiday[105].text
                        else:
                            yachtFishingGear = "<div class='nul'></div>"

                        if holiday[97].text:
                            yachtKiteBoarding = holiday[97].text
                        else:
                            yachtKiteBoarding = "<div class='nul'></div>"

                        if holiday[96].text:
                            yachtSeaScooter = holiday[96].text
                        else:
                            yachtSeaScooter = "<div class='nul'></div>"



                        if holiday[95].text:
                            yachtSeaBob = holiday[95].text
                        else:
                            yachtSeaBob = "<div class='nul'></div>"

                        if holiday[94].text :
                            yacht2ManKayak = holiday[94].text
                        else:
                            yacht2ManKayak = "<div class='nul'></div>"

                        if holiday[93].text :
                            yacht1ManKayak = holiday[93].text
                        else:
                            yacht1ManKayak = "<div class='nul'></div>"

                        if holiday[92].text:
                            yachtWakeBoard = holiday[92].text
                        else:
                            yachtWakeBoard = "<div class='nul'></div>"

                        if holiday[91].text :
                            yachtScurfer = holiday[91].text
                        else:
                            yachtScurfer = "<div class='nul'></div>"

                        if holiday[90].text:
                            yachtTube = holiday[90].text
                        else:
                            yachtTube = "<div class='nul'></div>"

                        if holiday[89].text:
                            yachtGearSnorkel = holiday[89].text
                        else:
                            yachtGearSnorkel = "<div class='nul'></div>"

                        if holiday[88].text:
                            yachtWindSurf = holiday[88].text
                        else:
                            yachtWindSurf = "<div class='nul'></div>"
                        if holiday[87].text :
                            yachtStandUpPaddle = holiday[87].text
                        else:
                            yachtStandUpPaddle = "<div class='nul'></div>"

                        if holiday[86].text:
                            yachtKneeBoard = holiday[86].text
                        else:
                            yachtKneeBoard = "<div class='nul'></div>"

                        if holiday[85].text:
                            yachtWaveRun = holiday[85].text
                        else:
                            yachtWaveRun = "<div class='nul'></div>"

                        if holiday[84].text:
                            yachtJetSkis = holiday[84].text
                        else:
                            yachtJetSkis = "<div class='nul'></div>"

                        if holiday[83].text :
                            yachtKidsSkis = holiday[83].text
                        else:
                            yachtKidsSkis = "<div class='nul'></div>"

                        if holiday[82].text :
                            yachtAdultWSkis = holiday[82].text
                        else:
                            yachtAdultWSkis = "<div class='nul'></div>"

                        if holiday[81].text :
                            yachtDinghyPax = holiday[81].text
                        else:
                            yachtDinghyPax = "<div class='nul'></div>"

                        if holiday[80].text:
                            yachtDinghyHp = holiday[80].text
                        else:
                            yachtDinghyHp = "<div class='nul'></div>"

                        if holiday[79].text:
                            yachtDinghy = holiday[79].text
                        else:
                            yachtDinghy = "<div class='nul'></div>"

                        val_watersports_hash = (
                            holiday[0].text, yachtDinghy, yachtDinghyHp, yachtDinghyPax, yachtAdultWSkis,
                            yachtKidsSkis,
                            yachtJetSkis, yachtWaveRun, yachtKneeBoard, yachtStandUpPaddle, yachtWindSurf,
                            yachtGearSnorkel,
                            yachtTube, yachtScurfer, yachtWakeBoard, yacht1ManKayak, yacht2ManKayak,
                            yachtSeaBob,
                            yachtSeaScooter, yachtKiteBoarding, yachtFishingGear, yachtFishGearType, yachtNumFishRods,
                            yachtDeepSeaFish,
                            yachtUnderWaterCam, yachtUnderWaterVideo)
                        if hashlib.md5(str(val_watersports_hash).encode("utf-8")).hexdigest() == boat_watersports_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από WaterSports")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από WaterSports</br>"
                        else:
                            print("Αλλαξε Κατι από WaterSports")
                            Boat_log = Boat_log + "Αλλαξε Κατι από WaterSports</br>"
                            mycursor.execute("DELETE FROM crew_water_sports WHERE id = " + str(int(boat_watersports_exist[0][2])))
                            boat_watersports_exist = mycursor.fetchall();



                            sql_watersports = "INSERT INTO `crew_water_sports` (`id`, `boat_id`, `yachtDinghy`, `yachtDinghyHp`, `yachtDinghyPax`, `yachtAdultWSkis`, `yachtKidsSkis`, `yachtJetSkis`, `yachtWaveRun`, `yachtKneeBoard`, `yachtStandUpPaddle`, `yachtWindSurf`, `yachtGearSnorkel`, `yachtTube`, `yachtScurfer`, `yachtWakeBoard`, `yacht1ManKayak`, `yacht2ManKayak`, `yachtSeaBob`, `yachtSeaScooter`, `yachtKiteBoarding`, `yachtFishingGear`, `yachtFishGearType`, `yachtNumFishRods`, `yachtDeepSeaFish`, `yachtUnderWaterCam`, `yachtUnderWaterVideo`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            val_watersports = (
                                holiday[0].text, yachtDinghy, yachtDinghyHp, yachtDinghyPax, yachtAdultWSkis,
                                yachtKidsSkis,
                                yachtJetSkis, yachtWaveRun, yachtKneeBoard, yachtStandUpPaddle, yachtWindSurf,
                                yachtGearSnorkel,
                                yachtTube, yachtScurfer, yachtWakeBoard, yacht1ManKayak, yacht2ManKayak,
                                yachtSeaBob,
                                yachtSeaScooter, yachtKiteBoarding, yachtFishingGear, yachtFishGearType, yachtNumFishRods,
                                yachtDeepSeaFish,
                                yachtUnderWaterCam, yachtUnderWaterVideo,
                                hashlib.md5(str(val_watersports_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_watersports, val_watersports)

                        # Check Characteristics of Crew Boats
                        mycursor.execute(
                            "SELECT boat_id, hash, id FROM crew_characteristics WHERE boat_id=" + holiday[0].text);
                        boat_character_exist = mycursor.fetchall();

                        if  holiday[38].text:
                            yachtAccommodations = holiday[38].text
                        else:
                            yachtAccommodations = "<div class='nul'></div>"

                        if  holiday[37].text:
                            yachtMaxSpeed = holiday[37].text
                        else:
                            yachtMaxSpeed = "<div class='nul'></div>"

                        if  holiday[36].text:
                            yachtCruiseSpeed = holiday[36].text
                        else:
                            yachtCruiseSpeed = "<div class='nul'></div>"

                        if  holiday[73].text:
                            yachtFuel = holiday[73].text
                        else:
                            yachtFuel = "<div class='nul'></div>"

                        if  holiday[72].text:
                            yachtEngines = holiday[72].text
                        else:
                            yachtEngines = "<div class='nul'></div>"


                        if  holiday[29].text:
                            yachtOtherPickup = holiday[29].text
                        else:
                            yachtOtherPickup = "<div class='nul'></div>"


                        if  holiday[28].text:
                            yachtPrefPickup = holiday[28].text
                        else:
                            yachtPrefPickup = "<div class='nul'></div>"


                        if  holiday[27].text:
                            yachtAc = holiday[27].text
                        else:
                            yachtAc = "<div class='nul'></div>"


                        if  holiday[22].text:
                            yachtJacuzzi = holiday[22].text
                        else:
                            yachtJacuzzi = "<div class='nul'></div>"

                        if  holiday[21].text:
                            yachtHelipad = holiday[21].text
                        else:
                            yachtHelipad = "<div class='nul'></div>"


                        if  holiday[178].text:
                            yachtElectricHeads = holiday[178].text
                        else:
                            yachtElectricHeads = "<div class='nul'></div>"

                        if holiday[177].text:
                            yachtHeads = holiday[177].text
                        else:
                            yachtHeads = "<div class='nul'></div>"

                        if holiday[176].text:
                            yachtWashBasins = holiday[176].text
                        else:
                            yachtWashBasins = "<div class='nul'></div>"

                        if holiday[268].text:
                            yachtTubs = holiday[268].text
                        else:
                            yachtTubs = "<div class='nul'></div>"


                        if holiday[175].text:
                            yachtShowers = holiday[175].text
                        else:
                            yachtShowers = "<div class='nul'></div>"





                        val_generic_hash = (
                            holiday[0].text, yachtShowers, yachtTubs, yachtWashBasins, yachtHeads,
                            yachtElectricHeads,
                            yachtHelipad, yachtJacuzzi, yachtAc, yachtPrefPickup, yachtOtherPickup,
                            yachtEngines, yachtFuel, yachtCruiseSpeed, yachtMaxSpeed, yachtAccommodations)
                        if hashlib.md5(str(val_generic_hash).encode("utf-8")).hexdigest() == boat_character_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από Characteristics")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Characteristics</br>"
                        else:
                            print("Αλλαξε Κατι από Characteristics")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Characteristics</br>"
                            mycursor.execute("DELETE FROM crew_characteristics WHERE id = " + str(int(boat_character_exist[0][2])))
                            boat_character_exist = mycursor.fetchall();
                            sql_generic = "INSERT INTO `crew_characteristics` (`id`, `boat_id`, `yachtShowers`, `yachtTubs`, `yachtWashBasins`, `yachtHeads`, `yachtElectricHeads`, `yachtHelipad`, `yachtJacuzzi`, `yachtAc`, `yachtPrefPickup`, `yachtOtherPickup`, `yachtEngines`, `yachtFuel`, `yachtCruiseSpeed`, `yachtMaxSpeed`, `yachtAccommodations`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            val_generic = (
                                holiday[0].text, yachtShowers, yachtTubs, yachtWashBasins, yachtHeads,
                                yachtElectricHeads,
                                yachtHelipad, yachtJacuzzi, yachtAc, yachtPrefPickup, yachtOtherPickup,
                                yachtEngines, yachtFuel, yachtCruiseSpeed, yachtMaxSpeed, yachtAccommodations,
                                hashlib.md5(str(val_generic_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_generic, val_generic)

                        # Checkt Crew Crewed
                        mycursor.execute(
                            "SELECT boat_id, hash, id FROM crew_boat_crewd WHERE boat_id=" + holiday[0].text);
                        boat_crewd_exist = mycursor.fetchall();

                        val_crew_hash = (
                            holiday[0].text, holiday[210].text, holiday[214].text, holiday[215].text, holiday[216].text,
                            holiday[220].text,
                            holiday[221].text, holiday[222].text, holiday[223].text, holiday[224].text,
                            holiday[229].text,
                            holiday[230].text, holiday[231].text, holiday[232].text, holiday[233].text,
                            holiday[234].text, holiday[235].text, holiday[236].text, holiday[237].text,
                            holiday[238].text, holiday[239].text, holiday[240].text,)
                        if hashlib.md5(str(val_crew_hash).encode("utf-8")).hexdigest() == boat_crewd_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από Crew Pliroma")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Crew Πλήρωμα</br>"
                        else:
                            print("Αλλαξε Κατι από Crew Pliroma")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Crew Πλήρωμα</br>"
                            mycursor.execute(
                                "DELETE FROM crew_boat_crewd WHERE id = " + str(int(boat_crewd_exist[0][2])))
                            boat_crewd_exist = mycursor.fetchall();
                            sql_crew = "INSERT INTO `crew_boat_crewd` (`id`, `boat_id`, `crew_num`, `yachtCaptainName`, `yachtCaptainNation`, `yachtCaptainBorn`, `yachtCaptainLang`, `yachtCrewName`, `yachtCrewTitle`, `yachtCrewNation`, `yachtCrewYrBorn`, `yachtCrewProfile`, `yachtCrewPhoto`, `yachtCrew1Pic`, `yachtCrew2Pic`, `yachtCrew3Pic`, `yachtCrew4Pic`, `yachtCrew5Pic`, `yachtCrew6Pic`, `yachtCrew7Pic`, `yachtCrew8Pic`, `yachtCrew9Pic`, `yachtCrew10Pic`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            val_crew = (
                                holiday[0].text, holiday[210].text, holiday[214].text, holiday[215].text,
                                holiday[216].text, holiday[220].text,
                                holiday[221].text, holiday[222].text, holiday[223].text, holiday[224].text,
                                holiday[229].text,
                                holiday[230].text, holiday[231].text, holiday[232].text, holiday[233].text,
                                holiday[234].text, holiday[235].text, holiday[236].text, holiday[237].text,
                                holiday[238].text, holiday[239].text, holiday[240].text,
                                hashlib.md5(str(val_crew_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_crew, val_crew)





                        #Check Videos of Crew

                        mycursor.execute(
                            "SELECT boat_id, hash, crw_video_id FROM crew_video_boats WHERE boat_id=" + holiday[0].text);
                        boat_video_exist = mycursor.fetchall();

                        video_val_hash = (holiday[0].text, holiday[35].text)
                        if hashlib.md5(str(video_val_hash).encode("utf-8")).hexdigest() == boat_video_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από Videos")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Videos</br>"
                        else:
                            print("Αλλαξε Κατι από Videos")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Videos</br>"
                            mycursor.execute("DELETE FROM crew_video_boats WHERE crw_video_id = " + str(int(boat_video_exist[0][2])))
                            boat_video_exist = mycursor.fetchall();
                            video_sql = "INSERT INTO `crew_video_boats` (`boat_id`, `video_url`, `hash`) VALUES (%s, %s, %s);"
                            video_val = (
                            holiday[0].text, holiday[35].text, hashlib.md5(str(video_val_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(video_sql, video_val)




                        # Check Manu  of Plan

                        mycursor.execute(
                            "SELECT boat_id, hash, plan_layout FROM crewd_plan WHERE boat_id=" + holiday[0].text);
                        boat_menu_exist = mycursor.fetchall();
                        print(boat_menu_exist)
                        menu_val_hash = (holiday[0].text, holiday[167].text)
                        if len(boat_menu_exist) > 0:
                            if hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest() == boat_menu_exist[0][1]:
                                print("Δεν Αλλαξε Κατι από Plan Layout")
                                Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Plan Layout</br>"
                            else:
                                print("Αλλαξε Κατι από Menu")
                                Boat_log = Boat_log + "Αλλαξε Κατι από Plan Layout</br>"
                                mycursor.execute(
                                    "DELETE FROM crewd_plan WHERE boat_id = " + str(int(holiday[0].text)))
                                boat_menu_exist = mycursor.fetchall();
                                menu_sql = "INSERT INTO `crewd_plan` (`boat_id`, `plan_layout`, `hash`) VALUES (%s, %s, %s);"
                                menu_val = (
                                    holiday[0].text, holiday[167].text,
                                    hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest())
                                mycursor.execute(menu_sql, menu_val)
                        else:
                            print("Αλλαξε Κατι από Menu")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Plan Layout</br>"

                            menu_sql = "INSERT INTO `crewd_plan` (`boat_id`, `plan_layout`, `hash`) VALUES (%s, %s, %s);"
                            menu_val = (
                                holiday[0].text, holiday[167].text,
                                hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(menu_sql, menu_val)

                        mycursor.execute(
                            "SELECT boat_id, hash FROM crewed_areas WHERE boat_id=" + holiday[0].text);
                        val_boat_destinations_exist = mycursor.fetchall();
                        val_boat_destinations_hash = (holiday[28].text, holiday[172].text, holiday[29].text)

                        if len(val_boat_destinations_exist) > 0:
                            if hashlib.md5(str(val_boat_destinations_hash).encode("utf-8")).hexdigest() == val_boat_destinations_exist[0][1]:
                                print("Δεν Αλλαξε Κατι από  Crewed Destinations")
                                Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Στο Crewed Destinations</br>"
                            else:
                                print("Αλλαξε Κατι από Menu")
                                Boat_log = Boat_log + "Αλλαξε Κατι από Crewed Destinations</br>"
                                mycursor.execute(
                                    "DELETE FROM crewed_areas WHERE boat_id = " + str(int(holiday[0].text)))
                                boat_menu_exist = mycursor.fetchall();
                                val_boat_destinations_sql = "INSERT INTO `crewed_areas` (`boat_id`, `yachtPrefPickup`, `yachtSummerArea`, `yachtOtherPickup`, `hash`) VALUES (%s, %s, %s, %s, %s);"
                                val_boat_destinations_val = (
                                holiday[0].text, holiday[28].text, holiday[173].text, holiday[29].text,
                                hashlib.md5(str(val_boat_destinations_hash).encode("utf-8")).hexdigest())
                                mycursor.execute(val_boat_destinations_sql, val_boat_destinations_val)

                        else:
                            print("Αλλαξε Κατι από Crewed Destinations")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Crewed Destinations</br>"
                            val_boat_destinations_sql = "INSERT INTO `crewed_areas` (`boat_id`, `yachtPrefPickup`, `yachtSummerArea`, `yachtOtherPickup`, `hash`) VALUES (%s, %s, %s, %s, %s);"
                            val_boat_destinations_val = (holiday[0].text, holiday[28].text, holiday[173].text, holiday[29].text,  hashlib.md5(str(val_boat_destinations_hash).encode("utf-8")).hexdigest())

                            mycursor.execute(val_boat_destinations_sql,  val_boat_destinations_val)
                            conn.commit()


                        # Check Manu  of Crew

                        mycursor.execute("SELECT boat_id, hash, menu_id FROM crew_sample_menu WHERE boat_id=" + holiday[0].text);
                        val_boat_menu_exist = mycursor.fetchall();

                        menu_val_hash = (holiday[0].text, holiday[199].text, holiday[200].text, holiday[201].text, holiday[202].text, holiday[203].text, holiday[204].text, holiday[205].text, holiday[206].text, holiday[207].text, holiday[208].text, holiday[209].text)
                        if len(val_boat_menu_exist) > 0:

                            if hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest() == val_boat_menu_exist[0][1]:
                                print("Δεν Αλλαξε Κατι από Menu")
                                Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Menu</br>"
                            else:
                                print("Αλλαξε Κατι από Menu")
                                Boat_log = Boat_log + "Αλλαξε Κατι από Menu</br>"
                                mycursor.execute("DELETE FROM crew_sample_menu WHERE menu_id = " + str(int(val_boat_menu_exist[0][2])))
                                boat_menu_exist = mycursor.fetchall();

                                menu_sql = "INSERT INTO `crew_sample_menu` (`boat_id`, `text_menu`, `yachtMenu1Pic`, `yachtMenu2Pic`, `yachtMenu3Pic`, `yachtMenu4Pic`, `yachtMenu5Pic`, `yachtMenu6Pic`, `yachtMenu7Pic`, `yachtMenu8Pic`, `yachtMenu9Pic`, `yachtMenu10Pic`, `hash`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                                menu_val = (
                                holiday[0].text, holiday[199].text, holiday[200].text, holiday[201].text, holiday[202].text,
                                holiday[203].text, holiday[204].text, holiday[205].text, holiday[206].text,
                                holiday[207].text, holiday[208].text, holiday[209].text,
                                hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest())
                                mycursor.execute(menu_sql, menu_val)
                        else:
                                print("Αλλαξε Κατι από Menu")
                                Boat_log = Boat_log + "Αλλαξε Κατι από Menu</br>"

                                menu_sql = "INSERT INTO `crew_sample_menu` (`boat_id`, `text_menu`, `yachtMenu1Pic`, `yachtMenu2Pic`, `yachtMenu3Pic`, `yachtMenu4Pic`, `yachtMenu5Pic`, `yachtMenu6Pic`, `yachtMenu7Pic`, `yachtMenu8Pic`, `yachtMenu9Pic`, `yachtMenu10Pic`, `hash`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                                menu_val = (
                                    holiday[0].text, holiday[199].text, holiday[200].text, holiday[201].text,
                                    holiday[202].text,
                                    holiday[203].text, holiday[204].text, holiday[205].text, holiday[206].text,
                                    holiday[207].text, holiday[208].text, holiday[209].text,
                                    hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest())
                                mycursor.execute(menu_sql, menu_val)

        except:
            pass


    print(Boat_log)
    sql_bases_log = "INSERT INTO `crew_boats_update_log` (`log`, `test`) VALUES (%s, %s);"
    val_bases_log  = (str(Boat_log), "test")
    mycursor.execute(sql_bases_log, val_bases_log)
    conn.commit()



    return "Done"









def crew_update_other():

    token = ""
    try:
        conn = mysql.connect(host='db39.grserver.gr', database='user7313393746_booking', user='fyly',
                             password='sd5w2V!0')
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            #cursor.execute('DROP TABLE IF EXISTS crew_boats;')
            #cursor.execute('DROP TABLE IF EXISTS crew_boats_basic;')

            # cursor.execute('DROP TABLE IF EXISTS boats_booking;')
            #cursor.execute('TRUNCATE TABLE crew_images_boats;')
            #cursor.execute('TRUNCATE TABLE crew_boat_crewd;')
            #cursor.execute('TRUNCATE TABLE crew_amenties;')
            #cursor.execute('TRUNCATE TABLE crew_water_sports;')
            #cursor.execute('TRUNCATE TABLE crew_characteristics;')
            #cursor.execute('TRUNCATE TABLE crew_video_boats;')
            #cursor.execute('TRUNCATE TABLE crew_yachtothertoys;')
            #cursor.execute('TRUNCATE TABLE crew_yachtotherentertain;')
            #cursor.execute('TRUNCATE TABLE crew_sample_menu;')
            print('Creating table....')
            # in the below line please pass the create table statement which you want #to create
            #cursor.execute("CREATE TABLE `user7313393746_booking`.`crew_boats` ( `id` INT NOT NULL AUTO_INCREMENT ,`boat_name` VARCHAR(255), `boat_category` VARCHAR(255), `boat_id` INT(11) NOT NULL , PRIMARY KEY (`id`))")
            print("Table crew_boats is created....")

            #cursor.execute("CREATE TABLE `user7313393746_booking`.`crew_boats_basic` (`id` INT NOT NULL AUTO_INCREMENT, `boat_id` INT(11) NOT NULL, `size` VARCHAR(255), `sizeft` VARCHAR(255), `yachtYearBuilt` VARCHAR(255), `yachtPax` INT(11), `yachtCabins` INT(11), `yachtCrew` INT(11), `yachtLowNumericPrice` FLOAT(11), `yachtHighNumericPrice` FLOAT(11), `yachtBuilder` VARCHAR(255), `yachtPrefPickup` VARCHAR(255), `yacht_description` LONGTEXT, `price_details` LONGTEXT, `location_details` LONGTEXT, `broker_notes` LONGTEXT, `hash` VARCHAR(255),  PRIMARY KEY (`id`))")
            print("Table crew_boats_basic  is created....")

            # cursor.execute(
            # "CREATE TABLE `user7313393746_booking`.`boats_booking` ( `book_id` INT NOT NULL AUTO_INCREMENT , `boat_id` INT(11) NOT NULL , `status` INT(11) NOT NULL , `datestart` VARCHAR(255) , `dateend` VARCHAR(255) , PRIMARY KEY (`book_id`))")
            # print("Table Boat Bookings is created....")






    except Error as e:
        print(e)

    import requests

    reqUrl = "http://www.centralyachtagent.com/snapins/snyachts-xml.php?user=1318&apicode=1318FYLY7hSs%d49hjQ"
    mycursor = conn.cursor()
    mycursor.execute('SELECT * FROM crew_boats_select WHERE is_fyly = 0')
    row_headers = [x[0] for x in mycursor.description]  # this will extract row headers
    rv = mycursor.fetchall()
    Boat_log = ""
    for result in rv:
       # print(result[1])
        reqUrl = "http://www.centralyachtagent.com/snapins/ebrochure-xml.php?user=1318&apicode=1318FYLY7hSs%d49hjQ&idin=" + str(
            result[1])

        payload = ""
        mycursor = conn.cursor()
        response = requests.request("GET", reqUrl, data=payload)
        import xml.etree.ElementTree as ET
        try:
            parser = ET.XMLParser(encoding="utf-8")
            xml = ET.fromstring(response.text, parser=parser)

            for holiday in xml.findall('yacht'):

                #print(len(holiday))
                if len(holiday) > 1:


                    mycursor.execute("SELECT boat_id, hash, id FROM crew_boats_basic WHERE boat_id=" + holiday[0].text);
                    boat_exist = mycursor.fetchall();
                    if (len(boat_exist) == 0):

                        sql = "INSERT INTO crew_boats (boat_name, boat_id, boat_category) VALUES (%s, %s, %s)"
                        print(holiday)
                        val = (holiday[1].text, holiday[0].text, holiday[4].text)
                        mycursor.execute(sql, val)

                        conn.commit();

                        crew_boats_basic_hash = (holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text, holiday[13].text,
                        holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text, holiday[28].text, holiday[130].text, holiday[269].text, holiday[271].text, holiday[284].text)


                        sql_extra = "INSERT  INTO `crew_boats_basic` (`id`, `boat_id`, `size`, `sizeft`, `yachtYearBuilt`, `yachtPax`, `yachtCabins`, `yachtCrew`, `yachtLowNumericPrice`, `yachtHighNumericPrice`, `yachtBuilder`, `yachtPrefPickup`, `yacht_description`, `price_details`, `location_details`, `broker_notes`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val_extra = (holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text, holiday[13].text,
                        holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text, holiday[28].text, holiday[130].text, holiday[269].text, holiday[271].text, holiday[284].text, hashlib.md5(str(crew_boats_basic_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_extra, val_extra)

                        image_count = 181
                        all_images = str(holiday[180].text)
                        while (image_count < 199):

                            if holiday[image_count].text:

                                all_images += "|" + holiday[image_count].text
                            image_count = image_count + 1

                        #Insert Images of Boat
                        val_images_hash = (holiday[0].text, holiday[180].text, all_images)
                        sql_images = "INSERT INTO `crew_images_boats` (`id`, `boat_id`, `image_crew`, `extra_images`, `hash`) VALUES (NULL, %s, %s, %s, %s);"
                        val_images = (holiday[0].text, holiday[180].text, all_images, hashlib.md5(str(val_images_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_images, val_images)


                        #Insert Entertaiment of Boat

                        val_yachtotherentertain_hash = (holiday[0].text, holiday[171].text)

                        sql_yachtotherentertain = "INSERT INTO `crew_yachtotherentertain` (`other_id`, `boat_id`, `yachtotherentertain`, `hash`) VALUES (NULL, %s, %s, %s);"
                        val_yachtotherentertain = (holiday[0].text, holiday[171].text, hashlib.md5(str(val_yachtotherentertain_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_yachtotherentertain, val_yachtotherentertain)

                        # Insert Other Toys  of Boat
                        val_othertoys_hash = (holiday[0].text, holiday[170].text)
                        sql_othertoys = "INSERT INTO `crew_yachtothertoys` (`id_other`, `boat_id`, `yachtothertoys`, `hash`) VALUES (NULL, %s, %s, %s);"
                        val_othertoys = (holiday[0].text, holiday[170].text, hashlib.md5(str(val_othertoys_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_othertoys, val_othertoys)

                        # Insert Amenities

                        val_amenties_hash = (
                        holiday[0].text, holiday[48].text, holiday[281].text, holiday[282].text, holiday[55].text, holiday[56].text,
                        holiday[57].text, holiday[58].text, holiday[59].text, holiday[60].text, holiday[61].text, holiday[62].text,
                        holiday[54].text, holiday[64].text, holiday[65].text, holiday[66].text, holiday[211].text, holiday[67].text,
                        holiday[68].text, holiday[69].text, holiday[23].text, holiday[25].text, holiday[26].text, holiday[71].text,
                        holiday[74].text, holiday[75].text, holiday[76].text, holiday[24].text, holiday[285].text, holiday[110].text,
                        holiday[111].text)
                        sql_amenties = "INSERT INTO `crew_amenties`(`amenties_id`, `boat_id`, `yachtSalonStereo`, `yachtSatTv`, `yachtIpod`, `yachtSunAwning`,`yachtHammock`, `yachtWindScoops`, `yachtDeckShower`, `yachtBimini`, `yachtSpecialDiets`, `yachtKosher`, `yachtBBQ`, `yachtNumDineIn`, `yachtNudeCharters`, `yachtHairDryer`, `yachtNumHatch`, `yachtCrewSmoke`, `yachtGuestSmoke`, `yachtGuestPet`, `yachtChildrenAllowed`, `yachtGym`, `yachtElevators`, `yachtWheelChairAccess`, `yachtGenerator`, `yachtInverter`, `yachtWaterMaker`, `yachtIceMaker`, `yachtStabilizers`, `yachtInternet`, `yachtGreenMakeWater`, `yachtGreenReuseBottle`, `hash`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)";
                        val_amenties = (
                        holiday[0].text, holiday[48].text, holiday[281].text, holiday[282].text, holiday[55].text, holiday[56].text,
                        holiday[57].text, holiday[58].text, holiday[59].text, holiday[60].text, holiday[61].text, holiday[62].text,
                        holiday[54].text, holiday[64].text, holiday[65].text, holiday[66].text, holiday[211].text, holiday[67].text,
                        holiday[68].text, holiday[69].text, holiday[23].text, holiday[25].text, holiday[26].text, holiday[71].text,
                        holiday[74].text, holiday[75].text, holiday[76].text, holiday[24].text, holiday[285].text, holiday[110].text,
                        holiday[111].text, hashlib.md5(str(val_amenties_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_amenties, val_amenties)



                        # Insert WaterSports of Crew Boats

                        val_watersports_hash = (
                        holiday[0].text, holiday[79].text, holiday[80].text, holiday[81].text, holiday[82].text, holiday[83].text,
                        holiday[84].text, holiday[85].text, holiday[86].text, holiday[87].text, holiday[88].text, holiday[89].text,
                        holiday[90].text, holiday[91].text, holiday[92].text, holiday[93].text, holiday[94].text, holiday[95].text,
                        holiday[96].text, holiday[97].text, holiday[105].text, holiday[106].text, holiday[107].text, holiday[280].text,
                        holiday[108].text, holiday[109].text)

                        sql_watersports = "INSERT INTO `crew_water_sports` (`id`, `boat_id`, `yachtDinghy`, `yachtDinghyHp`, `yachtDinghyPax`, `yachtAdultWSkis`, `yachtKidsSkis`, `yachtJetSkis`, `yachtWaveRun`, `yachtKneeBoard`, `yachtStandUpPaddle`, `yachtWindSurf`, `yachtGearSnorkel`, `yachtTube`, `yachtScurfer`, `yachtWakeBoard`, `yacht1ManKayak`, `yacht2ManKayak`, `yachtSeaBob`, `yachtSeaScooter`, `yachtKiteBoarding`, `yachtFishingGear`, `yachtFishGearType`, `yachtNumFishRods`, `yachtDeepSeaFish`, `yachtUnderWaterCam`, `yachtUnderWaterVideo`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        val_watersports = (
                        holiday[0].text, holiday[79].text, holiday[80].text, holiday[81].text, holiday[82].text, holiday[83].text,
                        holiday[84].text, holiday[85].text, holiday[86].text, holiday[87].text, holiday[88].text, holiday[89].text,
                        holiday[90].text, holiday[91].text, holiday[92].text, holiday[93].text, holiday[94].text, holiday[95].text,
                        holiday[96].text, holiday[97].text, holiday[105].text, holiday[106].text, holiday[107].text, holiday[280].text,
                        holiday[108].text, holiday[109].text, hashlib.md5(str(val_watersports_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_watersports, val_watersports)


                        # Insert Characteristics of Crew Boats

                        val_generic_hash = (
                        holiday[0].text, holiday[175].text, holiday[268].text, holiday[176].text, holiday[177].text, holiday[178].text,
                        holiday[21].text, holiday[22].text, holiday[27].text, holiday[28].text, holiday[29].text,
                        holiday[72].text, holiday[73].text, holiday[36].text, holiday[37].text, holiday[38].text)

                        sql_generic = "INSERT INTO `crew_characteristics` (`id`, `boat_id`, `yachtShowers`, `yachtTubs`, `yachtWashBasins`, `yachtHeads`, `yachtElectricHeads`, `yachtHelipad`, `yachtJacuzzi`, `yachtAc`, `yachtPrefPickup`, `yachtOtherPickup`, `yachtEngines`, `yachtFuel`, `yachtCruiseSpeed`, `yachtMaxSpeed`, `yachtAccommodations`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        val_generic = (
                        holiday[0].text, holiday[175].text, holiday[268].text, holiday[176].text, holiday[177].text, holiday[178].text,
                        holiday[21].text, holiday[22].text, holiday[27].text, holiday[28].text, holiday[29].text,
                        holiday[72].text, holiday[73].text, holiday[36].text, holiday[37].text, holiday[38].text, hashlib.md5(str(val_generic_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_generic, val_generic)

                        # Insert Crew Crewed
                        val_crew_hash = (
                        holiday[0].text, holiday[210].text, holiday[214].text, holiday[215].text, holiday[216].text, holiday[220].text,
                        holiday[221].text, holiday[222].text, holiday[223].text, holiday[224].text, holiday[229].text,
                        holiday[230].text, holiday[231].text)
                        sql_crew = "INSERT INTO `crew_boat_crewd` (`id`, `boat_id`, `crew_num`, `yachtCaptainName`, `yachtCaptainNation`, `yachtCaptainBorn`, `yachtCaptainLang`, `yachtCrewName`, `yachtCrewTitle`, `yachtCrewNation`, `yachtCrewYrBorn`, `yachtCrewProfile`, `yachtCrewPhoto`, `yachtCrew1Pic`, `yachtCrew2Pic`, `yachtCrew3Pic`, `yachtCrew4Pic`, `yachtCrew5Pic`, `yachtCrew6Pic`, `yachtCrew7Pic`, `yachtCrew8Pic`, `yachtCrew9Pic`, `yachtCrew10Pic`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                        val_crew = (
                        holiday[0].text, holiday[210].text, holiday[214].text, holiday[215].text, holiday[216].text, holiday[220].text,
                        holiday[221].text, holiday[222].text, holiday[223].text, holiday[224].text, holiday[229].text,
                        holiday[230].text, holiday[231].text, holiday[232].text, holiday[233].text, holiday[234].text, holiday[235].text, holiday[236].text, holiday[237].text, holiday[238].text, holiday[239].text, holiday[240].text, hashlib.md5(str(val_crew_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(sql_crew, val_crew)

                        # Insert Videos of Crew
                        video_val_hash = (holiday[0].text, holiday[35].text)
                        video_sql = "INSERT INTO `crew_video_boats` (`boat_id`, `video_url`, `hash`) VALUES (%s, %s, %s);"
                        video_val = (holiday[0].text, holiday[35].text, hashlib.md5(str(video_val_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(video_sql, video_val)
                        # Insert Menu of Crew
                        menu_val_hash = (holiday[0].text, holiday[199].text)
                        menu_sql = "INSERT INTO `crew_sample_menu` (`boat_id`, `text_menu`, `hash`) VALUES (%s, %s, %s);"
                        menu_val = (holiday[0].text, holiday[199].text, hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest())
                        mycursor.execute(menu_sql, menu_val)

                        conn.commit()

                    else:
                        #print(str(holiday.text))
                        print(boat_exist[0][0])

                        print(holiday[1].text)
                        Boat_log = Boat_log + "<h3>" + holiday[1].text + "</h3></br>";
                        crew_boats_basic_hash = (
                        holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text, holiday[13].text,
                        holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text, holiday[28].text,
                        holiday[130].text, holiday[269].text, holiday[271].text, holiday[286].text)

                        print(hashlib.md5(str(crew_boats_basic_hash).encode("utf-8")).hexdigest())
                        if hashlib.md5(str(crew_boats_basic_hash).encode("utf-8")).hexdigest() == boat_exist[0][1]:
                            print("Δεν Αλλαξε Κατι Specs")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι Specs</br>"
                        else:
                            print("Αλλαξε Κατι Specs")
                            Boat_log = Boat_log + "Αλλαξε Κατι Specs</br>"
                            mycursor.execute("DELETE FROM crew_boats_basic WHERE id = " + str(int(boat_exist[0][2])))
                            boat_exist = mycursor.fetchall();
                            crew_boats_basic_hash = (
                            holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text,
                            holiday[13].text,
                            holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text, holiday[28].text,
                            holiday[130].text, holiday[269].text, holiday[271].text, holiday[286].text)

                            sql_extra = "INSERT  INTO `crew_boats_basic` (`id`, `boat_id`, `size`, `sizeft`, `yachtYearBuilt`, `yachtPax`, `yachtCabins`, `yachtCrew`, `yachtLowNumericPrice`, `yachtHighNumericPrice`, `yachtBuilder`, `yachtPrefPickup`, `yacht_description`, `price_details`, `location_details`, `broker_notes`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            val_extra = (holiday[0].text, holiday[7].text, holiday[8].text, holiday[31].text, holiday[12].text,
                                         holiday[13].text,
                                         holiday[210].text, holiday[41].text, holiday[42].text, holiday[32].text,
                                         holiday[28].text, holiday[130].text, holiday[269].text, holiday[271].text,
                                         holiday[286].text, hashlib.md5(str(crew_boats_basic_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_extra, val_extra)
                            conn.commit()

                        #Check Images of Boat
                        mycursor.execute("SELECT boat_id, hash, id FROM crew_images_boats WHERE boat_id=" + holiday[0].text);
                        boat_images_exist = mycursor.fetchall();
                        image_count = 181
                        all_images = str(holiday[180].text)
                        while (image_count < 199):

                            if holiday[image_count].text:
                                all_images += "|" + holiday[image_count].text
                            image_count = image_count + 1



                        # Insert Images of Boat
                        val_images_hash = (holiday[0].text, holiday[180].text, all_images)
                        if hashlib.md5(str(val_images_hash).encode("utf-8")).hexdigest() == boat_images_exist[0][1]:
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Φωτογραφίες</br>"
                            print("Δεν Αλλαξε Κατι από Φωτογραφίες")
                        else:
                            print("Αλλαξε Κατι από Φωτογραφίες")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Φωτογραφίες</br>"
                            mycursor.execute("DELETE FROM crew_images_boats WHERE id = " + str(int(boat_images_exist[0][2])))
                            boat_images_exist = mycursor.fetchall();
                            sql_images = "INSERT INTO `crew_images_boats` (`id`, `boat_id`, `image_crew`, `extra_images`, `hash`) VALUES (NULL, %s, %s, %s, %s);"
                            val_images = (holiday[0].text, holiday[180].text, all_images,
                                          hashlib.md5(str(val_images_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_images, val_images)

                        #Check Entertaiment of Boat
                        mycursor.execute("SELECT boat_id, hash, other_id FROM crew_yachtotherentertain WHERE boat_id=" + holiday[0].text);
                        boat_entertain_exist = mycursor.fetchall();

                        val_yachtotherentertain_hash = (holiday[0].text, holiday[171].text)

                        if hashlib.md5(str(val_yachtotherentertain_hash).encode("utf-8")).hexdigest() == boat_entertain_exist[0][1]:
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Entertain</br>"
                            print("Δεν Αλλαξε Κατι από Entertain")
                        else:
                            print("Αλλαξε Κατι από Entertain")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Entertain</br>"
                            mycursor.execute("DELETE FROM crew_yachtotherentertain WHERE other_id = " + str(int(boat_entertain_exist[0][2])))
                            boat_entertain_exist = mycursor.fetchall();
                            sql_yachtotherentertain = "INSERT INTO `crew_yachtotherentertain` (`other_id`, `boat_id`, `yachtotherentertain`, `hash`) VALUES (NULL, %s, %s, %s);"
                            val_yachtotherentertain = (holiday[0].text, holiday[171].text,
                                                       hashlib.md5(str(val_yachtotherentertain_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_yachtotherentertain, val_yachtotherentertain)

                        # Check Other Toys of Boat
                        mycursor.execute(
                            "SELECT boat_id, hash, id_other FROM crew_yachtothertoys WHERE boat_id=" + holiday[0].text);
                        boat_othertoys_exist = mycursor.fetchall();
                        val_othertoys_hash = (holiday[0].text, holiday[170].text)
                        # Insert Other Toys  of Boat
                        if hashlib.md5(str(val_othertoys_hash).encode("utf-8")).hexdigest() == boat_othertoys_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από Other Toys")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Other Toys</br>"
                        else:
                            print("Αλλαξε Κατι από Other Toys")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Other Toys</br>"
                            mycursor.execute("DELETE FROM crew_yachtothertoys WHERE id_other = " + str(int(boat_othertoys_exist[0][2])))
                            boat_othertoys_exist = mycursor.fetchall();
                            sql_othertoys = "INSERT INTO `crew_yachtothertoys` (`id_other`, `boat_id`, `yachtothertoys`, `hash`) VALUES (NULL, %s, %s, %s);"
                            val_othertoys = (
                            holiday[0].text, holiday[170].text, hashlib.md5(str(val_othertoys_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_othertoys, val_othertoys)

                            # Insert Amenities

                        mycursor.execute(
                            "SELECT boat_id, hash, amenties_id FROM crew_amenties WHERE boat_id=" + holiday[0].text);
                        boat_amenties_exist = mycursor.fetchall();

                        val_amenties_hash = (
                            holiday[0].text, holiday[48].text, holiday[281].text, holiday[282].text, holiday[55].text,
                            holiday[56].text,
                            holiday[57].text, holiday[58].text, holiday[59].text, holiday[60].text, holiday[61].text,
                            holiday[62].text,
                            holiday[54].text, holiday[64].text, holiday[65].text, holiday[66].text, holiday[211].text,
                            holiday[67].text,
                            holiday[68].text, holiday[69].text, holiday[23].text, holiday[25].text, holiday[26].text,
                            holiday[71].text,
                            holiday[74].text, holiday[75].text, holiday[76].text, holiday[24].text, holiday[285].text,
                            holiday[110].text,
                            holiday[111].text)

                        if hashlib.md5(str(val_amenties_hash).encode("utf-8")).hexdigest() == boat_amenties_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από amenties")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από amenties</br>"
                        else:
                            print("Αλλαξε Κατι από amenties")
                            Boat_log = Boat_log + "Αλλαξε Κατι από amenties</br>"
                            mycursor.execute("DELETE FROM crew_amenties WHERE amenties_id = " + str(int(boat_amenties_exist[0][2])))
                            boat_amenties_exist = mycursor.fetchall();
                            sql_amenties = "INSERT INTO `crew_amenties`(`amenties_id`, `boat_id`, `yachtSalonStereo`, `yachtSatTv`, `yachtIpod`, `yachtSunAwning`,`yachtHammock`, `yachtWindScoops`, `yachtDeckShower`, `yachtBimini`, `yachtSpecialDiets`, `yachtKosher`, `yachtBBQ`, `yachtNumDineIn`, `yachtNudeCharters`, `yachtHairDryer`, `yachtNumHatch`, `yachtCrewSmoke`, `yachtGuestSmoke`, `yachtGuestPet`, `yachtChildrenAllowed`, `yachtGym`, `yachtElevators`, `yachtWheelChairAccess`, `yachtGenerator`, `yachtInverter`, `yachtWaterMaker`, `yachtIceMaker`, `yachtStabilizers`, `yachtInternet`, `yachtGreenMakeWater`, `yachtGreenReuseBottle`, `hash`) VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)";
                            val_amenties = (
                                holiday[0].text, holiday[48].text, holiday[281].text, holiday[282].text, holiday[55].text,
                                holiday[56].text,
                                holiday[57].text, holiday[58].text, holiday[59].text, holiday[60].text, holiday[61].text,
                                holiday[62].text,
                                holiday[54].text, holiday[64].text, holiday[65].text, holiday[66].text, holiday[211].text,
                                holiday[67].text,
                                holiday[68].text, holiday[69].text, holiday[23].text, holiday[25].text, holiday[26].text,
                                holiday[71].text,
                                holiday[74].text, holiday[75].text, holiday[76].text, holiday[24].text, holiday[285].text,
                                holiday[110].text,
                                holiday[111].text, hashlib.md5(str(val_amenties_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_amenties, val_amenties)

                        # Check WaterSports of Crew Boats
                        mycursor.execute(
                            "SELECT boat_id, hash, id FROM crew_water_sports WHERE boat_id=" + holiday[0].text);
                        boat_watersports_exist = mycursor.fetchall();
                        val_watersports_hash = (
                            holiday[0].text, holiday[79].text, holiday[80].text, holiday[81].text, holiday[82].text,
                            holiday[83].text,
                            holiday[84].text, holiday[85].text, holiday[86].text, holiday[87].text, holiday[88].text,
                            holiday[89].text,
                            holiday[90].text, holiday[91].text, holiday[92].text, holiday[93].text, holiday[94].text,
                            holiday[95].text,
                            holiday[96].text, holiday[97].text, holiday[105].text, holiday[106].text, holiday[107].text,
                            holiday[280].text,
                            holiday[108].text, holiday[109].text)
                        if hashlib.md5(str(val_watersports_hash).encode("utf-8")).hexdigest() == boat_watersports_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από WaterSports")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από WaterSports</br>"
                        else:
                            print("Αλλαξε Κατι από WaterSports")
                            Boat_log = Boat_log + "Αλλαξε Κατι από WaterSports</br>"
                            mycursor.execute("DELETE FROM crew_water_sports WHERE id = " + str(int(boat_watersports_exist[0][2])))
                            boat_watersports_exist = mycursor.fetchall();

                            sql_watersports = "INSERT INTO `crew_water_sports` (`id`, `boat_id`, `yachtDinghy`, `yachtDinghyHp`, `yachtDinghyPax`, `yachtAdultWSkis`, `yachtKidsSkis`, `yachtJetSkis`, `yachtWaveRun`, `yachtKneeBoard`, `yachtStandUpPaddle`, `yachtWindSurf`, `yachtGearSnorkel`, `yachtTube`, `yachtScurfer`, `yachtWakeBoard`, `yacht1ManKayak`, `yacht2ManKayak`, `yachtSeaBob`, `yachtSeaScooter`, `yachtKiteBoarding`, `yachtFishingGear`, `yachtFishGearType`, `yachtNumFishRods`, `yachtDeepSeaFish`, `yachtUnderWaterCam`, `yachtUnderWaterVideo`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            val_watersports = (
                                holiday[0].text, holiday[79].text, holiday[80].text, holiday[81].text, holiday[82].text,
                                holiday[83].text,
                                holiday[84].text, holiday[85].text, holiday[86].text, holiday[87].text, holiday[88].text,
                                holiday[89].text,
                                holiday[90].text, holiday[91].text, holiday[92].text, holiday[93].text, holiday[94].text,
                                holiday[95].text,
                                holiday[96].text, holiday[97].text, holiday[105].text, holiday[106].text, holiday[107].text,
                                holiday[280].text,
                                holiday[108].text, holiday[109].text,
                                hashlib.md5(str(val_watersports_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_watersports, val_watersports)

                        # Check Characteristics of Crew Boats
                        mycursor.execute(
                            "SELECT boat_id, hash, id FROM crew_characteristics WHERE boat_id=" + holiday[0].text);
                        boat_character_exist = mycursor.fetchall();
                        val_generic_hash = (
                            holiday[0].text, holiday[175].text, holiday[268].text, holiday[176].text, holiday[177].text,
                            holiday[178].text,
                            holiday[21].text, holiday[22].text, holiday[27].text, holiday[28].text, holiday[29].text,
                            holiday[72].text, holiday[73].text, holiday[36].text, holiday[37].text, holiday[38].text)
                        if hashlib.md5(str(val_generic_hash).encode("utf-8")).hexdigest() == boat_character_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από Characteristics")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Characteristics</br>"
                        else:
                            print("Αλλαξε Κατι από Characteristics")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Characteristics</br>"
                            mycursor.execute("DELETE FROM crew_characteristics WHERE id = " + str(int(boat_character_exist[0][2])))
                            boat_character_exist = mycursor.fetchall();
                            sql_generic = "INSERT INTO `crew_characteristics` (`id`, `boat_id`, `yachtShowers`, `yachtTubs`, `yachtWashBasins`, `yachtHeads`, `yachtElectricHeads`, `yachtHelipad`, `yachtJacuzzi`, `yachtAc`, `yachtPrefPickup`, `yachtOtherPickup`, `yachtEngines`, `yachtFuel`, `yachtCruiseSpeed`, `yachtMaxSpeed`, `yachtAccommodations`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            val_generic = (
                                holiday[0].text, holiday[175].text, holiday[268].text, holiday[176].text, holiday[177].text,
                                holiday[178].text,
                                holiday[21].text, holiday[22].text, holiday[27].text, holiday[28].text, holiday[29].text,
                                holiday[72].text, holiday[73].text, holiday[36].text, holiday[37].text, holiday[38].text,
                                hashlib.md5(str(val_generic_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_generic, val_generic)

                        # Checkt Crew Crewed
                        mycursor.execute(
                            "SELECT boat_id, hash, id FROM crew_boat_crewd WHERE boat_id=" + holiday[0].text);
                        boat_crewd_exist = mycursor.fetchall();


                        val_crew_hash = (
                            holiday[0].text, holiday[210].text, holiday[214].text, holiday[215].text, holiday[216].text,
                            holiday[220].text,
                            holiday[221].text, holiday[222].text, holiday[223].text, holiday[224].text, holiday[229].text,
                            holiday[230].text, holiday[231].text, holiday[232].text, holiday[233].text,
                                holiday[234].text, holiday[235].text, holiday[236].text, holiday[237].text,
                                holiday[238].text, holiday[239].text, holiday[240].text,)
                        if hashlib.md5(str(val_crew_hash).encode("utf-8")).hexdigest() == boat_crewd_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από Crew Pliroma")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Crew Πλήρωμα</br>"
                        else:
                            print("Αλλαξε Κατι από Crew Pliroma")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Crew Πλήρωμα</br>"
                            mycursor.execute("DELETE FROM crew_boat_crewd WHERE id = " + str(int(boat_crewd_exist[0][2])))
                            boat_crewd_exist = mycursor.fetchall();
                            sql_crew = "INSERT INTO `crew_boat_crewd` (`id`, `boat_id`, `crew_num`, `yachtCaptainName`, `yachtCaptainNation`, `yachtCaptainBorn`, `yachtCaptainLang`, `yachtCrewName`, `yachtCrewTitle`, `yachtCrewNation`, `yachtCrewYrBorn`, `yachtCrewProfile`, `yachtCrewPhoto`, `yachtCrew1Pic`, `yachtCrew2Pic`, `yachtCrew3Pic`, `yachtCrew4Pic`, `yachtCrew5Pic`, `yachtCrew6Pic`, `yachtCrew7Pic`, `yachtCrew8Pic`, `yachtCrew9Pic`, `yachtCrew10Pic`, `hash`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                            val_crew = (
                                holiday[0].text, holiday[210].text, holiday[214].text, holiday[215].text,
                                holiday[216].text, holiday[220].text,
                                holiday[221].text, holiday[222].text, holiday[223].text, holiday[224].text,
                                holiday[229].text,
                                holiday[230].text, holiday[231].text, holiday[232].text, holiday[233].text,
                                holiday[234].text, holiday[235].text, holiday[236].text, holiday[237].text,
                                holiday[238].text, holiday[239].text, holiday[240].text,
                                hashlib.md5(str(val_crew_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(sql_crew, val_crew)





                        #Check Videos of Crew

                        mycursor.execute(
                            "SELECT boat_id, hash, crw_video_id FROM crew_video_boats WHERE boat_id=" + holiday[0].text);
                        boat_video_exist = mycursor.fetchall();

                        video_val_hash = (holiday[0].text, holiday[35].text)
                        if hashlib.md5(str(video_val_hash).encode("utf-8")).hexdigest() == boat_video_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από Videos")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Videos</br>"
                        else:
                            print("Αλλαξε Κατι από Videos")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Videos</br>"
                            mycursor.execute("DELETE FROM crew_video_boats WHERE crw_video_id = " + str(int(boat_video_exist[0][2])))
                            boat_video_exist = mycursor.fetchall();
                            video_sql = "INSERT INTO `crew_video_boats` (`boat_id`, `video_url`, `hash`) VALUES (%s, %s, %s);"
                            video_val = (
                            holiday[0].text, holiday[35].text, hashlib.md5(str(video_val_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(video_sql, video_val)

                        # Check Manu  of Crew

                        mycursor.execute("SELECT boat_id, hash, menu_id FROM crew_sample_menu WHERE boat_id=" + holiday[0].text);
                        boat_menu_exist = mycursor.fetchall();

                        menu_val_hash = (holiday[0].text, holiday[199].text)
                        if hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest() == boat_menu_exist[0][1]:
                            print("Δεν Αλλαξε Κατι από Menu")
                            Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Menu</br>"
                        else:
                            print("Αλλαξε Κατι από Menu")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Menu</br>"
                            mycursor.execute("DELETE FROM crew_sample_menu WHERE menu_id = " + str(int(boat_menu_exist[0][2])))
                            boat_menu_exist = mycursor.fetchall();
                            menu_sql = "INSERT INTO `crew_sample_menu` (`boat_id`, `text_menu`, `hash`) VALUES (%s, %s, %s);"
                            menu_val = (
                            holiday[0].text, holiday[199].text, hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(menu_sql, menu_val)

                        mycursor.execute(
                            "SELECT boat_id, hash, plan_layout FROM crewd_plan WHERE boat_id=" + holiday[0].text);
                        boat_menu_exist = mycursor.fetchall();
                        print(boat_menu_exist)
                        menu_val_hash = (holiday[0].text, holiday[167].text)
                        if len(boat_menu_exist) > 0:
                            if hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest() == boat_menu_exist[0][1]:
                                print("Δεν Αλλαξε Κατι από Plan Layout")
                                Boat_log = Boat_log + "Δεν Αλλαξε Κατι από Plan Layout</br>"
                            else:
                                print("Αλλαξε Κατι από Menu")
                                Boat_log = Boat_log + "Αλλαξε Κατι από Plan Layout</br>"
                                mycursor.execute(
                                    "DELETE FROM crewd_plan WHERE boat_id = " + str(int(holiday[0].text)))
                                boat_menu_exist = mycursor.fetchall();
                                menu_sql = "INSERT INTO `crewd_plan` (`boat_id`, `plan_layout`, `hash`) VALUES (%s, %s, %s);"
                                menu_val = (
                                    holiday[0].text, holiday[167].text,
                                    hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest())
                                mycursor.execute(menu_sql, menu_val)
                        else:
                            print("Αλλαξε Κατι από Menu")
                            Boat_log = Boat_log + "Αλλαξε Κατι από Plan Layout</br>"

                            menu_sql = "INSERT INTO `crewd_plan` (`boat_id`, `plan_layout`, `hash`) VALUES (%s, %s, %s);"
                            menu_val = (
                                holiday[0].text, holiday[167].text,
                                hashlib.md5(str(menu_val_hash).encode("utf-8")).hexdigest())
                            mycursor.execute(menu_sql, menu_val)

        except:
            pass


    print(Boat_log)
    sql_bases_log = "INSERT INTO `crew_boats_update_log` (`log`, `test`) VALUES (%s, %s);"
    val_bases_log  = (str(Boat_log), "test")
    mycursor.execute(sql_bases_log, val_bases_log)
    conn.commit()



    return "Done"


