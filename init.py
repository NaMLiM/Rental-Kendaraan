import os
import platform
import random
import time

import mysql.connector as mysql

# Console Initialization
os.system("title Rental Kendaraan")
os.system("color 1F")
if platform.system() == "Windows":
    def clearcmd():
        os.system("cls")
elif platform.system() == "Linux":
    def clearcmd():
        os.system("clear")
cursor, db = None, None


def animated_loading(text, i, num=None):
    loading_char = "|/-\|"
    if num is True:
        for char in range(100 + 1):
            print("\r" + text + "..." + str(char) + "%", end="")
            time.sleep(i)
    else:
        for char in loading_char:
            print("\r" + text + "..." + str(char), end="")
            time.sleep(i)


def connect_db():
    global db, cursor
    while True:
        animated_loading("SYS: Menghubungkan", random.uniform(0.3, 0.7))
        try:
            db = mysql.connect(host="localhost", user="root", passwd="", database="rental")
            cursor = db.cursor()
            if db:
                print("\rSYS: Koneksi Database Sukses!")
                break
        except mysql.errors.DatabaseError:
            print("\rSYS: Koneksi Database Gagal!")
            for i in range(5, 0, -1):
                print("\rSYS: Mencoba Lagi Dalam " + str(i), end="")
                time.sleep(1)


animated_loading("SYS: Loading App", 0.010, True)
print("\r" + "SYS: Loading App Sukses!")
connect_db()
