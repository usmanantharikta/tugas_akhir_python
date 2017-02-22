import serial #load library for read serial data from arduino
import pymysql.cursors #load library for connect to databases mysql
from tabulate import tabulate #import library for print result query on Table
from datetime import date #import date
from datetime import datetime #import date time
import hashlib #import hashlib

#connect to databases mysql
def connect_db():
    connection = pymysql.connect(host='localhost',
                         user='root',
                         password='antharikta',
                         db='db_ta',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)

#function read RFID Tag from serial communication
def rfid_reader():
    ser = serial.Serial('/dev/ttyUSB0', 9600) #read serial data from port TTYUSB0 with boundrate 9600
    flag=True;
    while flag:
        id_book=ser.readline()
        id_book=ser.read(14)
        print("++++++++++++++++++++++++++++ Result ++++++++++++++++++++++++++++++")
        print("The ID of this card is: "+ str(id_book))
        input_option=input("Are You Sure will use this ID (y/n) c to main Menu ) :")
        if(input_option=='y'or input_option=='Y'):
            return id_book
            flag=False
        elif(input_option=="c" or input_option=="C"):
            break
        else:
            print("______________________________________________________________")
            print("Please Scan New Card !!!")

#save to data bases
def save_new_book(data):
    connection = pymysql.connect(host='localhost',
                         user='root',
                         password='antharikta',
                         db='db_ta',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `book_master` (`id_rfid`, `book_title`, `author`,`publisher`,`editor`,`year`,`description`,`price`,`input_date`,`book_status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,data )
            connection.commit()
            sekarang = datetime.today()
            reg_time=sekarang.strftime('%Y-%m-%d %H:%M:%S')
            reg_card="INSERT INTO card (rfid_id,reg_time, use_for) VALUES (%s, %s, %s )"
            cursor.execute(reg_card,(data[0],reg_time,"book"))
            connection.commit()
        print("New Data has been save !!!!")

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `book_master` where `id_rfid`=%s "
            cursor.execute(sql,data[0])
            result=cursor.fetchall()
            print("______________________ Data On Databases___________________________")
            print(tabulate(result,headers="keys",tablefmt="orgtbl"))
    finally:
        connection.close()

#save new member to databases
def save_new_member(data_member):
    connection = pymysql.connect(host='localhost',
                         user='root',
                         password='antharikta',
                         db='db_ta',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `user_master` (`id_rfid`,`username`,`email`,`password`,`first_name`,`last_name`,`phone`,`gender`,`birthday`,`register_date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,data_member)
            connection.commit()
            sekarang = datetime.today()
            reg_time=sekarang.strftime('%Y-%m-%d %H:%M:%S')
            reg_card="INSERT INTO card (rfid_id,reg_time, use_for) VALUES (%s, %s, %s )"
            cursor.execute(reg_card,(data_member[0],reg_time,"member"))
            connection.commit()
            print("New Data has been save !!!!")

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `user_master` where `id_rfid`=%s "
            cursor.execute(sql,data_member[0])
            result=cursor.fetchall()
            print("______________________ Data On Databases___________________________")
            print(tabulate(result))
    finally:
        connection.close()
#cek to databases
def cek_to_databases(id_rfid):
    connection = pymysql.connect(host='localhost',
                         user='root',
                         password='antharikta',
                         db='db_ta',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql_book="SELECT * FROM `book_master` where `id_rfid`=%s "
            cursor.execute(sql_book,id_rfid)
            result_book=cursor.fetchall()

            if(result_book):
                print("-----------------------------------Result of Databases from Book table ----------------------------------")
                print(tabulate(result_book))
                return

            else:
                sql_member="SELECT * FROM `user_master` where `id_rfid`=%s "
                cursor.execute(sql_member,id_rfid)
                result_member=cursor.fetchall()
                if(result_member):
                    print("--------------------------------Result of Database from User Tabel -----------------------------------")
                    print(tabulate(result_member))
                else:
                    print("ID card is not ready use or Missing data")
                    return
    finally:
        connection.close()

#funtion add new book
def add_new_book():
    print("                                                              ")
    print("##################### ADD NEW BOOK ###########################")
    print("                                                              ")
    print("Please Tap RFID Tag to RFID Reader !!!")
    id_rfid=rfid_reader() #call function for read ID RFID from Arduino
    if(id_rfid==None): #if ID of RFID is none return to main menu
        return
    print("______________________________________________________________")
    print("+++++++++++++++++++++ Form Add New Book ++++++++++++++++++++++")
    print("ID RFID : "+ str(id_rfid))
    book_title=input("Book Title: ")
    author=input("Author : ")
    publisher=input("Publisher : ")
    editor=input("Editor : ")
    year=input("Year : ")
    description=input("Description : ")
    price=input("Price : ")
    now = date.today()
    print("++++++++++++++++++End of Form Add New Book +++++++++++++++++++")
    print("                                                              ")
    print("___________________ Detail of New Book _______________________")
    data_book=[["ID RFID ",id_rfid],["Book Title ",book_title],["Author ",author],["Publisher ",publisher],["Editor ",editor],["Year ",year],["Description ",description],["Price ",price],["Date Input", now.strftime("%y/%m/%d")]]
    data=(id_rfid,book_title,author,publisher,editor,year,description,price,now.strftime("%y/%m/%d"),"0")
    print(tabulate(data_book))
    save=input("Are You Sure to Save this data to databases (y/n) : ")
    if(save=="y" or save=="Y"):
        save_new_book(data)
    else:
        return
    print("_______________________________________________________________")

#add new member
def add_new_member():
    print("                                                              ")
    print("##################### ADD NEW MEMBER #########################")
    print("                                                              ")
    print("Please Tap RFID Tag to RFID Reader !!!")
    id_rfid_member=rfid_reader() #call function for read ID RFID from Arduino
    if(id_rfid_member==None): #if ID of RFID is none return to main menu
        return
    print("______________________________________________________________")
    print("+++++++++++++++++++++ Form Add New Member ++++++++++++++++++++++")
    print("ID RFID : "+ str(id_rfid_member))
    username=input("User Name : ")
    email=input("Email : ")
    first_name=input("First Name : ")
    last_name=input("Last Name : ")
    phone=input("Phone : ")
    gender=input("Gende (male/female) : ")
    birthday=input("Birth Day (yyyy/mm/dd) : ")
    register_date = date.today()
    print("++++++++++++++++++End of Form Add New Book +++++++++++++++++++")
    print("                                                              ")
    print("___________________ Detail of New Member are You Input _______________________")
    data_member=[['ID RFID ',id_rfid_member],['User Name ',username],['email',email],['First Name ',first_name],['Last Name',last_name],['Phone ',phone],['Gender',gender],['Birth Day',birthday],['Register date',register_date.strftime("%y/%m/%d")]]
    data_array_member=(id_rfid_member,username,email,hashlib.sha224(id_rfid_member).hexdigest(),first_name,last_name,phone,gender,birthday,register_date.strftime("%y/%m/%y"))
    print(tabulate(data_member))
    save_member=input("Are You Sure to Save this data to databases (y/n) : ")
    if(save_member=="y" or save_member=="Y"):
        save_new_member(data_array_member)
    else:
        return
    print("_______________________________________________________________")

#cek id
def cek_id_rfid():
    print("                                                              ")
    print("##################### ADD NEW MEMBER #########################")
    print("                                                              ")
    print("Please Tap RFID Tag to RFID Reader !!!")
    id_rfid=rfid_reader() #call function for read ID RFID from Arduino
    if(id_rfid==None): #if ID of RFID is none return to main menu
        return
    print("______________________________________________________________")
    cek_to_databases(id_rfid)


#MENU
while True:
    print("                                                              ")
    print("########################### MENU #############################")
    print("1. Add New Book ")
    print("2. Add New Member ")
    print("3. Cek ID Card")
    print("4. View Book Table ")
    print("5. Exit")
    print("______________________________________________________________")
    option=int(input("Input Your Option : "))#get input user for select menu
    print("______________________________________________________________")

    #condition
    # menu 1 add new book
    if(option==1):
        add_new_book() #call function add new book to databases

    #menu 2 add new member
    if(option==2):
        add_new_member() # call function add new member to database

    #menu 3 cek id card on data bases
    if(option==3):
        cek_id_rfid() #call function to check rfid tag on data bases

    #menu 5 exit
    if(option==5):
        exit("Bye Bye Baby !!!")
