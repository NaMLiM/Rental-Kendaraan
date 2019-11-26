from prettytable import PrettyTable

from init import *

listAksi = PrettyTable()
listAksiKendaraan = PrettyTable()
listAksiRental = PrettyTable()
listAksiPeminjam = PrettyTable()
listKendaraan = PrettyTable()

def login():
    global login_status, username
    login_status = None
    print()
    while True:
        if login_status == None:
            print("==========Login==========")
            username = input("Masukkan Username: ")
            password = input("Masukkan Password: ")
            cursor.execute("select * from pegawai where username=%s and password=%s", (username, password))
            animated_loading("Login", random.uniform(0.3, 0.5))
            if cursor.fetchone():
                login_status = "Logged In"
                print("\rSYS: Logged In")
            else:
                print("\rSYS: Username/Password Salah!")
                print()
            print("=========================")
        else:
            break
    print()
    time.sleep(2)
    animated_loading("SYS: Fetching Data", random.uniform(0.3, 0.5))
    print("\rSYS: Fetching Data Complete")
    animated_loading("Loading Data", 0.010, True)
    print("\rSYS: Loading Data Complete")
    print()
    time.sleep(2)
    clearcmd()
    print("Selamat Datang", username)

def logout():
    global login_status
    login_status = None
    animated_loading("SYS: Logging Out", random.uniform(0.3, 0.5))
    print("\rSYS: Logged Out Successfully")
    time.sleep(3)
    clearcmd()
    login()

def main():
    global login_status
    global cursor
    if login_status == None:
        login()
    # tabel listAksi
    listAksi.field_names = ["Aksi"]
    listAksi.add_row(["1.Opsi Kendaraan"])
    listAksi.add_row(["2.Opsi Rental"])
    listAksi.add_row(["3.Opsi Peminjam"])
    listAksi.add_row(["4.Logout"])
    # tabel listAksiKendaraan
    listAksiKendaraan.field_names = ["Aksi Tabel Kendaraan"]
    listAksiKendaraan.add_row(["1.List Kendaraan"])
    listAksiKendaraan.add_row(["2.Kembali"])
    # tabel listKendaraan
    listKendaraan.field_names = ["No", "Nama Kendaraan", "Merk Kendaraan", "Jenis Kendaraan", "Jumlah Kendaraan"]
    while True:
        print(listAksi)
        pilih = int(input("Masukkan Aksi | "))
        if pilih == 1:
            clearcmd()
            print(listAksiKendaraan)
            pilih = int(input("Masukkan Aksi | "))
            if pilih == 1:
                clearcmd()
                cursor.execute("select * from kendaraan")
                result = cursor.fetchall()
                for i in range(len(result)):
                    listKendaraan.add_row(result[i])
                print(listKendaraan)
                listKendaraan.clear_rows()
            else:
                clearcmd()
                break
        elif pilih == 4:
            logout()
        else:
            print("Aksi Tidak Valid")
            print()

if __name__ == '__main__':
    main()
