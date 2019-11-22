import os
import platform
import random
import sys
import time

# Console Initialization
os.system("title Rental Kendaraan")
os.system("color 1F")
if platform.system() == "Windows":
    clearcmd = lambda: os.system("cls")
elif platform.system() == "Linux":
    clearcmd = lambda: os.system("clear")


def animated_loading(text, i, num=None):
    loading_char = "|/-\|"
    if num == True:
        for char in range(100 + 1):
            sys.stdout.write('\r' + text + '...' + str(char) + "%")
            time.sleep(i)
    else:
        for char in loading_char:
            sys.stdout.write('\r' + text + '...' + str(char))
            time.sleep(i)


def connect_db():
    global db, cursor
    while True:
        animated_loading("SYS: Menghubungkan", random.uniform(0.3, 0.7))
        try:
            import mysql.connector as mysql
            db = mysql.connect(host="localhost", user="root", passwd="", database="rental")
            cursor = db.cursor()
            if db:
                print("\rSYS: Koneksi Database Sukses!")
                break
        except:
            print("\rSYS: Koneksi Database Gagal!")
            for i in range(5, 0, -1):
                sys.stdout.write('\r' + "SYS: Mencoba Lagi Dalam " + str(i))
                time.sleep(1)


animated_loading("SYS: Loading App", 0.010, True)
print("\r" + "SYS: Loading App Sukses!")
connect_db()
