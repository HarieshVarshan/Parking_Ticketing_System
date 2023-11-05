import mysql.connector
from mysql.connector import Error
import logging
import pyfiglet
import os, re
import getpass
from enum import Enum
from datetime import datetime, timedelta
import random

class status(Enum):
    PARKING_FULL = 1,
    INVALID_VEHICLE_NO = 2,
    INVALID_PHONE_NO = 3,
    VEHICLE_ALREADY_INSIDE = 4,


class flag(Enum): # check items
    FINISH_PROCESS = 1,
    
    # checks for vehicle entry
    ENTRY_GET_4W_2W = 2,
    ENTRY_CHECK_PARKING_FULL = 3,
    ENTRY_GET_VEHICLE_PHONE_NUM = 4,
    ENTRY_ADD_NEW_VEHICLE = 5,
    ENTRY_UPDATE_SLOT_AND_CREATE_TICKET = 6,
    ENTRY_UPDATE_SLOT_AND_CREATE_TICKET_AUTH = 7,

    # checks for vehicle exit
    EXIT_GET_VEHICLE_NUM = 8,
    EXIT_RECORD_TIME = 9,
    EXIT_COST_CALCULATION = 10,
    EXIT_FREE_THE_SLOT = 11,



class common:
    TEST_ENV = 1
    logging.disable(logging.ERROR)

    @staticmethod
    def runQuery(query):
        records = None
        attributes = None
        db = None
        cursor = None
        try:
            # Create a connection to the database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="welcome",
                database="parking_ticketing_system"
            )

            # Create a cursor object
            cursor = db.cursor(buffered=True)

            # Execute sql query
            cursor.execute(query)

            # Commit changes to the database
            db.commit()

            # Fetch all the rows/records
            try:
                records = cursor.fetchall()
                # get column names
                attributes = [column[0] for column in cursor.description]
            
            except Exception as e:
                logging.error("query returned nothing. msg: %s", e)
            
        except Error as e:
            logging.error("error while connecting to mySQL. msg: %s", e)

        finally:
            # Close the connection
            if cursor is not None:
                cursor.close()
            if db is not None and db.is_connected():
                db.close()
            return records, attributes

    @staticmethod
    def runProc(proc, params):
        records = None
        attributes = None
        db = None
        cursor = None
        try:
            # Create a connection to the database
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="welcome",
                database="parking_ticketing_system"
            )

            # Create a cursor object
            cursor = db.cursor(buffered=True)

            # Execute sql query
            cursor.callproc(proc, params)

            # Commit changes to the database
            db.commit()

            # Fetch all the rows/records
            try:
                for result in cursor.stored_results():
                    records = result.fetchall()
                
                # get column names
                attributes = [column[0] for column in cursor.description]
            
            except Exception as e:
                print("query returned nothing. msg:", e)
                logging.error("query returned nothing. msg: %s", e)
            
        except Error as e:
            print("error while connecting to mySQL. msg: ", e)
            logging.error("error while connecting to mySQL. msg: %s", e)

        finally:
            # Close the connection
            if cursor is not None:
                cursor.close()
            if db is not None and db.is_connected():
                db.close()
            return records, attributes


    @staticmethod
    def beautify(rows, columns):
        # find the maximum length of value in each column
        column_widths = [len(name) for name in columns]
        for row in rows:
            for i, value in enumerate(row):
                column_widths[i] = max(column_widths[i], len(str(value)))

        # print column names
        print('+ ' + ' + '.join([f"{'-'*w:{w}}" for w in column_widths]) + ' +')
        print('+ ' + ' + '.join([f"{str(name):{w}}" for name, w in zip(columns, column_widths)]) + ' +')
        print('+ ' + ' + '.join([f"{'-'*w:{w}}" for w in column_widths]) + ' +')

        # print rows
        for each_row in rows:
            print('| ' + ' | '.join([f"{str(value):{w}}" for value, w in zip(each_row, column_widths)]) + ' |')
        print('+ ' + ' + '.join([f"{'-'*w:{w}}" for w in column_widths]) + ' +')


    @staticmethod
    def beautify_query(msg):
        # find the maximum length of value in each column
        w = len(msg)

        top = '+ ' + f"{'-'*w:{w}}" + ' +'
        get_input = '| ' + f"{str(msg):{w}}" + ' |'
        bottom = '+ ' + f"{'-'*w:{w}}" + ' +'

        return '\n'.join([top, get_input, bottom]) + '\n'

    @staticmethod
    def checkEmpty(rows=None):
        if rows == None or rows == []:
            return True
        else:
            return False
        
    @staticmethod
    def validateVehicleNum(_vNum):
        # regex pattern for Indian vehicle registration numbers
        pattern = r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$'
        if not re.match(pattern, _vNum):
            print("Invalid Vehicle Number!!")
            return False
        return True

    @staticmethod
    def checkAuthVehicle(_vNum):
        rows, columns = common.runQuery(f"SELECT vNum FROM authorized_vehicle WHERE vNum='{_vNum}';")
        if not common.checkEmpty(rows):
            return True
        return False



class app:
    current_user = None
    current_pwd = None

    options = {
        "1": "vehicleEntry",
        "2": "vehicleExit",
        "3": "availableSlots",
        "4": "filledSlots",
        "5": "incomeStats",
        "6": "vehicleHistory",
        "7": "lookUp",
        "8": "customerStats",
        "9": "exitApp",
    }

    admin_options = {
        "90": "updateSlotForMaintenance",
        "91": "makeMaintenanceSlotAvailable",
        "92": "addMoreSlots",
    }


    def switcher(action):
        selected_option = app.options.get(action)

        rows, columns = common.runQuery(f"SELECT empType FROM employee WHERE username='{app.current_user}';")
        if selected_option == None and not common.checkEmpty(rows) and rows[0][0] == "admin":
            selected_option = app.admin_options.get(action)
        
        getattr(app, selected_option)() if selected_option else print(common.beautify_query("Invalid Option, Try again!"))


    def vehicleEntry(state = flag.ENTRY_GET_4W_2W):
        while (state != flag.FINISH_PROCESS):
            if state == flag.ENTRY_GET_4W_2W:
                _vType = input("Is it a car? (y/n): ").lower()
                _vType = '4w' if _vType == 'y' else '2w'
                state = flag.ENTRY_CHECK_PARKING_FULL
            
            elif state == flag.ENTRY_CHECK_PARKING_FULL:
                rows, columns = common.runQuery(f"SELECT sID FROM slot WHERE sType = 'public' AND status = 'free' AND vType = '{_vType}' ORDER BY sID ASC LIMIT 1;")
                if not common.checkEmpty(rows):
                    state = flag.ENTRY_GET_VEHICLE_PHONE_NUM
                    _sID = rows[0][0]
                else:
                    print("Parking is Full!!")
                    state = flag.FINISH_PROCESS
            
            elif state == flag.ENTRY_GET_VEHICLE_PHONE_NUM:
                _vNum = input("Enter Vehicle Number: ").upper()
                if(not common.validateVehicleNum(_vNum)):
                    state = flag.FINISH_PROCESS
                    continue

                if common.checkAuthVehicle(_vNum):
                    state = flag.ENTRY_UPDATE_SLOT_AND_CREATE_TICKET_AUTH
                    continue

                rows, columns = common.runQuery(f"SELECT vNum FROM slot WHERE vNum = '{_vNum}';")
                if not common.checkEmpty(rows):
                    print("This vehicle is already parked inside!!")
                    state = flag.FINISH_PROCESS
                    continue

                rows, columns = common.runQuery(f"SELECT * FROM contact_info WHERE vNum='{_vNum}';")
                if common.checkEmpty(rows):
                    _phNo = input("Enter Phone Number: ")
                    if not _phNo.isdigit():
                        print("Invalid Phone Number!!")
                        state = flag.FINISH_PROCESS
                        continue
                    state = flag.ENTRY_ADD_NEW_VEHICLE
                else:
                    print("Already a happy customer :)")
                    state = flag.ENTRY_UPDATE_SLOT_AND_CREATE_TICKET

            elif state == flag.ENTRY_ADD_NEW_VEHICLE:
                common.runQuery(f"INSERT INTO vehicle (vNum, vType) VALUES ('{_vNum}', '{_vType}');")
                common.runQuery(f"INSERT INTO contact_info (vNum, phoneNum) VALUES ('{_vNum}', '{_phNo}');")
                state = flag.ENTRY_UPDATE_SLOT_AND_CREATE_TICKET

            elif state == flag.ENTRY_UPDATE_SLOT_AND_CREATE_TICKET:
                common.runQuery(f"UPDATE slot SET status = 'occupied', vNum = '{_vNum}', updatedBy = '{app.current_user}' WHERE sID = '{_sID}';")
                if common.TEST_ENV == 1:
                    _start_date = datetime(2023, 10, 1, 0, 0, 0)
                    _end_date = datetime(2023, 10, 29, 23, 59, 59)
                    _entry_time = _start_date + timedelta(seconds=random.randint(0, int((_end_date - _start_date).total_seconds())))
                    _exit_time = _entry_time + timedelta(seconds=random.randint(3600, 36000))
                    common.runQuery(f"INSERT INTO entries (vNum, entryTime, exitTime) VALUES ('{_vNum}', '{_entry_time}', '{_exit_time}');")
                else:
                    common.runQuery(f"INSERT INTO entries (vNum, entryTime) VALUES ('{_vNum}', NOW());")
                state = flag.FINISH_PROCESS
                print("Slot assigned and Ticket created!!")
            
            elif state == flag.ENTRY_UPDATE_SLOT_AND_CREATE_TICKET_AUTH:
                rows, columns = common.runQuery(f"SELECT sID FROM slot WHERE status='free' AND sType='authorized';")
                if common.checkEmpty(rows):
                    print("Authorized Vehicle Parking Full!!")
                    state = flag.FINISH_PROCESS
                    continue

                _sID = rows[0][0]
                common.runQuery(f"UPDATE slot SET status = 'occupied', vNum = '{_vNum}', updatedBy = '{app.current_user}' WHERE sID = '{_sID}';")
                state = flag.FINISH_PROCESS
                print("Slot assigned for Authorized Vehicles")


    def vehicleExit(state = flag.EXIT_GET_VEHICLE_NUM):
        while state != flag.FINISH_PROCESS:
            if state == flag.EXIT_GET_VEHICLE_NUM:
                _vNum = input("Exit Vehicle Number: ").upper()
                if(not common.validateVehicleNum(_vNum)):
                    state = flag.FINISH_PROCESS
                    continue

                if common.checkAuthVehicle(_vNum):
                    state = flag.EXIT_FREE_THE_SLOT
                    continue

                rows, columns = common.runQuery(f"SELECT vNum FROM slot WHERE vNum='{_vNum}';")
                if common.checkEmpty(rows):
                    print("This vehicle did not even enter!!")
                    state = flag.FINISH_PROCESS
                else:
                    state = flag.EXIT_RECORD_TIME

            elif state == flag.EXIT_RECORD_TIME:
                if common.TEST_ENV == 0:
                    common.runQuery(f"UPDATE entries SET exitTime = NOW() WHERE vNum='{_vNum}';")
                state = flag.EXIT_COST_CALCULATION

            elif state == flag.EXIT_COST_CALCULATION:
                rows, columns = common.runQuery(f"SELECT vType FROM slot WHERE vNum='{_vNum}';")
                _vType = rows[0][0]
                if _vType == '2w':
                    cost_per_hour = 20.0
                elif _vType == '4w':
                    cost_per_hour = 40.0
                
                query = f"""
                    SELECT 
                    TIMESTAMPDIFF(HOUR, entryTime, exitTime) AS hours,
                    MOD(TIMESTAMPDIFF(MINUTE, entryTime, exitTime), 60) AS minutes
                    FROM entries WHERE vNum='{_vNum}' ORDER BY eID DESC LIMIT 1;
                """
                rows, columns = common.runQuery(query)
                _hours = rows[0][0]
                _minutes = rows[0][1]
                _cost = _hours * cost_per_hour + (_minutes/60) * cost_per_hour
                print("[BP]",_hours, _minutes, _cost)
                common.runQuery(f"UPDATE entries SET cost = '{_cost:.1f}' WHERE vNum='{_vNum}' ORDER BY eID DESC LIMIT 1;")
                print(f"Amount to be paid Rs.{_cost:.1f}")
                state = flag.EXIT_FREE_THE_SLOT

            elif state == flag.EXIT_FREE_THE_SLOT:
                common.runQuery(f"UPDATE slot SET status = 'free', vNum = NULL, updatedBy = '{app.current_user}' WHERE vNum = '{_vNum}';")
                print("Thank You, Visit Again!!")
                state = flag.FINISH_PROCESS
            

    def availableSlots():
        rows, columns = common.runQuery(f"SELECT COUNT(*) FROM slot WHERE status='free' AND vType='2w' AND sType='public';")
        _free_slots_count_2w = rows[0][0]
        rows, columns = common.runQuery(f"SELECT COUNT(*) FROM slot WHERE status='free' AND vType='4w'AND sType='public';")
        _free_slots_count_4w = rows[0][0]
        rows, columns = common.runQuery(f"SELECT COUNT(*) FROM slot WHERE vType='2w'AND sType='public';")
        _total_slots_2w = rows[0][0]
        rows, columns = common.runQuery(f"SELECT COUNT(*) FROM slot WHERE vType='4w'AND sType='public';")
        _total_slots_4w = rows[0][0]
        common.beautify(rows=[(f"{_free_slots_count_2w}/{_total_slots_2w}", f"{_free_slots_count_4w}/{_total_slots_4w}")], columns=["Free 2w slots count", "Free 4w slots count"])


    def filledSlots():
        rows, columns = common.runQuery(f"SELECT COUNT(*) FROM slot WHERE status='occupied' AND vType='2w' AND sType='public';")
        _flld_slots_count_2w = rows[0][0]
        rows, columns = common.runQuery(f"SELECT COUNT(*) FROM slot WHERE status='occupied' AND vType='4w'AND sType='public';")
        _flld_slots_count_4w = rows[0][0]
        rows, columns = common.runQuery(f"SELECT COUNT(*) FROM slot WHERE vType='2w'AND sType='public';")
        _total_slots_2w = rows[0][0]
        rows, columns = common.runQuery(f"SELECT COUNT(*) FROM slot WHERE vType='4w'AND sType='public';")
        _total_slots_4w = rows[0][0]
        common.beautify(rows=[(f"{_flld_slots_count_2w}/{_total_slots_2w}", f"{_flld_slots_count_4w}/{_total_slots_4w}")], columns=["Filled 2w slots count", "Filled 4w slots count"])


    def incomeStats():
        def incomeSwitcher(income_action):
            selected_option = income_stat_options.get(income_action)
            selected_option() if selected_option else print(common.beautify_query("Invalid Option, Try again!"))

        def incomeGeneratedSoFar():
            query = f"""
                    SELECT SUM(cost) AS 'Income Generated So Far (in Rs.)' FROM entries;
                    """
            rows, columns = common.runQuery(query)
            common.beautify(rows, columns)
        
        def incomeBwDateRange():
            _start_date = input("Enter Start Date (yyyy-mm-dd): ")
            _end_date = input("Enter End Date (yyyy-mm-dd): ")
            query = f"""
                    SELECT DATE(exitTime) AS 'Date', SUM(cost) AS 'Total Income (in Rs.)'
                    FROM entries
                    WHERE DATE(exitTime) >= '{_start_date}' AND DATE(exitTime) < DATE('{_end_date}' + INTERVAL 1 DAY)
                    GROUP BY Date;
                    """
            rows, columns = common.runQuery(query)
            common.beautify(rows, columns)
        
        def incomeFromAVehicleType():
            query = f"""
                    SELECT v.vType AS 'Vehicle Type', SUM(e.cost) AS 'Total Income (in Rs.)'
                    FROM entries e JOIN vehicle v ON e.vNum = v.vNum
                    GROUP BY v.vType;
                    """
            rows, columns = common.runQuery(query)
            common.beautify(rows, columns)

        def incomeFromAVehicle():
            _vNum = input("Enter Vehicle Number: ").upper()
            if(not common.validateVehicleNum(_vNum)):
                return
            query = f"""
                    SELECT v.vNum AS 'Vehicle Number', SUM(e.cost) AS 'Total Income (in Rs.)'
                    FROM entries e JOIN vehicle v ON e.vNum = v.vNum
                    WHERE v.vNum = '{_vNum}';
                    """
            rows, columns = common.runQuery(query)
            common.beautify(rows, columns)

        def incomeOnAGivenDay():
            _date = input("Enter Date (yyyy-mm-dd): ")
            query = f"""
                    SELECT DATE(exitTime) AS 'Date', SUM(cost) AS 'Total Income (in Rs.)'
                    FROM entries
                    WHERE DATE(exitTime) = '{_date}'
                    GROUP BY Date;
                    """
            rows, columns = common.runQuery(query)
            common.beautify(rows, columns)

        def backToDashboard():
            pass

        income_stat_options = {
            "1": incomeGeneratedSoFar,
            "2": incomeBwDateRange,
            "3": incomeFromAVehicleType,
            "4": incomeFromAVehicle,
            "5": incomeOnAGivenDay,
            "6": backToDashboard,
        }
        
        def incomeRunLoop():
            income_action = None
            while(income_action != "6"): # backToDashboard
                # clear screen
                os.system('cls' if os.name == 'nt' else 'clear')

                # print menu
                print(pyfiglet.figlet_format("Income Stats"))
                common.beautify([[f"{key}. {value.__name__}"] for key, value in income_stat_options.items()], ["Income Stat Options"])

                income_action = input("Enter option: ")

                # execute action
                incomeSwitcher(income_action)

                # wait for user input to continue
                if income_action != "6":
                    input("Continue? (Press Enter)")

        incomeRunLoop()


    def vehicleHistory():
        _vNum = input("Enter Vehicle Number: ")
        if(not common.validateVehicleNum(_vNum)):
            return
        query = f"""
                SELECT vNum, entryTime, exitTime
                FROM entries
                WHERE vNum="{_vNum}";
                """
        rows, columns = common.runQuery(query)
        common.beautify(rows, columns)


    def lookUp():
        def lookupSwitcher(lookup_action):
            selected_option = lookup_stat_options.get(lookup_action)
            selected_option() if selected_option else print(common.beautify_query("Invalid Option, Try again!"))

        def lookupSlotFromVehicleNum():
            _vNum = input("Enter Vehicle Number to find the slot: ")
            if(not common.validateVehicleNum(_vNum)):
                return
            rows, columns = common.runQuery(f"SELECT vNum, sID from slot WHERE vNum='{_vNum}';")
            common.beautify(rows, columns)

        def lookupVehicleFromSlotNum():
            _sID = input("Enter Slot Number to find the vehicle: ")
            rows, columns = common.runQuery(f"SELECT sID, vNum from slot WHERE sID='{_sID}';")
            common.beautify(rows, columns)
        
        def lookupAllSlots():
            rows, columns = common.runQuery(f"SELECT sID, vNum, vType, sType from slot WHERE status='occupied';")
            common.beautify(rows, columns)

        def backToDashboard():
            pass

        lookup_stat_options = {
            "1": lookupSlotFromVehicleNum,
            "2": lookupVehicleFromSlotNum,
            "3": lookupAllSlots,
            "4": backToDashboard,
        }
        
        def lookupRunLoop():
            lookup_action = None
            while(lookup_action != "4"): # backToDashboard
                # clear screen
                os.system('cls' if os.name == 'nt' else 'clear')

                # print menu
                print(pyfiglet.figlet_format("Lookup"))
                common.beautify([[f"{key}. {value.__name__}"] for key, value in lookup_stat_options.items()], ["lookup Stat Options"])

                lookup_action = input("Enter option: ")

                # execute action
                lookupSwitcher(lookup_action)

                # wait for user input to continue
                if lookup_action != "4":
                    input("Continue? (Press Enter)")

        lookupRunLoop()


    def customerStats():
        def customerSwitcher(customer_action):
            selected_option = customer_stat_options.get(customer_action)
            selected_option() if selected_option else print(common.beautify_query("Invalid Option, Try again!"))

        def customersSoFar():
            query = f"""
                    SELECT COUNT(eID) AS 'Customers So Far' FROM entries;
                    """
            rows, columns = common.runQuery(query)
            common.beautify(rows, columns)
        
        def customersBwDateRange():
            _start_date = input("Enter Start Date (yyyy-mm-dd): ")
            _end_date = input("Enter End Date (yyyy-mm-dd): ")
            query = f"""
                    SELECT DATE(exitTime) AS 'Date', COUNT(eID) AS 'No of. Customers'
                    FROM entries
                    WHERE DATE(exitTime) >= '{_start_date}' AND DATE(exitTime) < DATE('{_end_date}' + INTERVAL 1 DAY)
                    GROUP BY Date;
                    """
            rows, columns = common.runQuery(query)
            common.beautify(rows, columns)
        
        def customersBasedOnVehicleType():
            query = f"""
                    SELECT v.vType AS 'Vehicle Type', COUNT(e.eID) AS 'No of. Customers'
                    FROM entries e JOIN vehicle v ON e.vNum = v.vNum
                    GROUP BY v.vType;
                    """
            rows, columns = common.runQuery(query)
            common.beautify(rows, columns)

        def customersOnAGivenDay():
            _date = input("Enter Date (yyyy-mm-dd): ")
            query = f"""
                    SELECT DATE(exitTime) AS 'Date', COUNT(eID) AS 'No of. Customers'
                    FROM entries
                    WHERE DATE(exitTime) = '{_date}'
                    GROUP BY Date;
                    """
            rows, columns = common.runQuery(query)
            common.beautify(rows, columns)

        def backToDashboard():
            pass

        customer_stat_options = {
            "1": customersSoFar,
            "2": customersBwDateRange,
            "3": customersBasedOnVehicleType,
            "4": customersOnAGivenDay,
            "5": backToDashboard,
        }
        
        def customerRunLoop():
            customer_action = None
            while(customer_action != "5"): # backToDashboard
                # clear screen
                os.system('cls' if os.name == 'nt' else 'clear')

                # print menu
                print(pyfiglet.figlet_format("customer Stats"))
                common.beautify([[f"{key}. {value.__name__}"] for key, value in customer_stat_options.items()], ["customer Stat Options"])

                customer_action = input("Enter option: ")

                # execute action
                customerSwitcher(customer_action)

                # wait for user input to continue
                if customer_action != "5":
                    input("Continue? (Press Enter)")

        customerRunLoop()


    def login():
        login_successful = False
        while(not login_successful):
            print(common.beautify_query("Enter your credentials to login: "))
            app.current_user = input("Username: ")
            app.current_pwd = getpass.getpass('Password: ')

            rows, columns = common.runQuery(f"SELECT username, pwd_hash FROM employee WHERE username='{app.current_user}' AND pwd_hash=SHA2('{app.current_pwd}',256);")
            
            if common.checkEmpty(rows):
                print(common.beautify_query("Invalid Username or Password"))
                input("Retry Again..")
                # clear screen
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                login_successful = True


    def updateSlotForMaintenance():
        _sID = input("Enter Slot ID For Maintenance: ")
        rows, columns = common.runQuery(f"SELECT sID FROM slot WHERE status='occupied'AND sID='{_sID}';")
        if common.checkEmpty(rows):
            common.runQuery(f"UPDATE slot SET status='maintenance' WHERE sID='{_sID}';")
        else:
            print("This Slot is not Free!!")
        pass


    def makeMaintenanceSlotAvailable():
        _sID = input("Enter Slot ID: ")
        rows, columns = common.runQuery(f"SELECT sID FROM slot WHERE status='maintenance'AND sID='{_sID}';")
        if common.checkEmpty(rows):
            print("This Slot ID is not under Maintenance!!")
        else:
            common.runQuery(f"UPDATE slot SET status='free' WHERE sID='{_sID}';")


    def addMoreSlots():
        _vType = input("Is it for Car? (y/n) ")
        _vType = '4w' if _vType == 'y' else '2w'
        _start = int(input("Enter Starting Slot ID: "))
        _end = int(input("Enter Ending Slot ID: "))
        common.runProc("addNewSlots", (_start, _end, _vType, 'public'))
        print(f"Added {_end - _start + 1} New Slots!!")


    def runLoop():
        app.login()
        while(1):
            # clear screen
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # print menu
            print(pyfiglet.figlet_format("Parking Ticketing System"))
            common.beautify([[f"{key}. {value}"] for key, value in app.options.items()], ["Options"])

            rows, columns = common.runQuery(f"SELECT empType FROM employee WHERE username='{app.current_user}';")
            if not common.checkEmpty(rows) and rows[0][0] == "admin":
                common.beautify([[f"{key}. {value}"] for key, value in app.admin_options.items()], ["Admin Only Options"])

            # take input
            action = input("Enter option: ")
            
            # execute action
            app.switcher(action)

            # wait for user input to continue
            input("Continue? (Press Enter)")


    def exitApp():
        print(pyfiglet.figlet_format("Bye!"))
        exit(0)
    


class test:
    @staticmethod
    def quickInsert(startID, endID, prefix1, prefix2, _vType):
        is_auth = 0
        if prefix1[0:2] == "AU":
            is_auth = 1
        for _sID in range(startID, endID + 1):
            _vNum = f"{prefix1}{_sID:04}"
            _phNum = f"{prefix2}{_sID:09}"
            if is_auth == 0:
                common.runQuery(f"INSERT INTO vehicle (vNum, vType) VALUES ('{_vNum}', '{_vType}');")
                common.runQuery(f"INSERT INTO contact_info (vNum, phoneNum) VALUES ('{_vNum}', '{_phNum}');")
            common.runQuery(f"UPDATE slot SET status = 'occupied', vNum = '{_vNum}', updatedBy = 'vrshn' WHERE sID = '{_sID}';")


    @staticmethod
    def makeParkingFull():
        test.quickInsert(1, 100, "PB37CR", "1", "4w")
        test.quickInsert(101, 180, "PB37BK", "2", "2w")
        test.quickInsert(181, 190, "AU37CR", "3", "4w")
        test.quickInsert(191, 200, "AU37BK", "4", "2w")


# test.makeParkingFull()
app.runLoop()

