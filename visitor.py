import serial #load library for read serial data from arduino
import pymysql.cursors #load library for connect to databases mysql
from tabulate import tabulate #import library for print result query on Table
from datetime import datetime #import date

#function cek rfid
def cek_user(rfid):
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='antharikta',
                                 db='db_ta',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql="SELECT * FROM user_master where id_rfid=%s"
            cursor.execute(sql,rfid)
            result=cursor.fetchone()
            if(result):
                print("\n")
                print("Welcome "+str(result["username"])+" !!!!!")
                print("\n")
                now = datetime.today()
                insert="INSERT INTO log_visitor (user_id, rfid, log_time) VALUES (%s, %s, %s)"
                cursor.execute(insert,(result["user_id"],result['id_rfid'],now.strftime('%Y-%m-%d %H:%M:%S')))
                connection.commit()
    finally:
        connection.close()

ser = serial.Serial('/dev/ttyUSB0', 9600) #read serial data from port TTYUSB0 with boundrate 9600
while True:
    print("Please Tap Your Card !!!! ")
    rfid=ser.readline()
    rfid=ser.read(14)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    #print("The ID of this card is: "+ str(rfid))
    cek_user(rfid)
    rfid=0
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
