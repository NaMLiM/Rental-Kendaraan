from prettytable import PrettyTable

from init import *


def login():
    global login_status, username
    print()
    while True:
        if login_status is None:
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
    global login_status, cursor
    if login_status is None:
        login()

    listaksi = PrettyTable()
    listaksikendaraan = PrettyTable()
    listaksirental = PrettyTable()
    listaksipeminjam = PrettyTable()
    listkendaraan = PrettyTable()
    listrental = PrettyTable()

    data = PrettyTable()
    data.title = "Data"

    # tabel listaksi
    listaksi.field_names = ["Aksi"]
    listaksi.add_row(["1.Opsi Kendaraan"])
    listaksi.add_row(["2.Opsi Rental"])
    listaksi.add_row(["3.Opsi Peminjam"])
    listaksi.add_row(["4.Logout"])

    # tabel listaksirental
    listaksirental.field_names = ["Aksi Tabel Rental"]
    listaksirental.add_row(["1.Rental Kendaraan"])
    listaksirental.add_row(["2.List Rental"])
    listaksirental.add_row(["3.Kembali"])

    # tabel listaksikendaraan
    listaksikendaraan.field_names = ["Aksi Tabel Kendaraan"]
    listaksikendaraan.add_row(["1.List Kendaraan"])
    listaksikendaraan.add_row(["2.Kembali"])

    # tabel listaksipeminjam
    listaksipeminjam.field_names = ["Aksi Tabel Peminjam"]
    listaksipeminjam.add_row(["1.Daftarkan Peminjam"])
    listaksipeminjam.add_row(["2.List Peminjam"])
    listaksipeminjam.add_row(["3.Kembali"])

    while True:
        print(listaksi)
        pilih = int(input("Masukkan Aksi | "))
        if pilih == 1:
            clearcmd()
            listkendaraan.field_names = ["No", "Nama Kendaraan", "Merk Kendaraan",
                                         "Jenis Kendaraan", "Jumlah Kendaraan"]
            print(listaksikendaraan)
            pilih = int(input("Masukkan Aksi | "))
            if pilih == 1:
                clearcmd()
                cursor.execute("select * from kendaraan")
                result = cursor.fetchall()
                for i in range(len(result)):
                    listkendaraan.add_row(result[i])
                print(listkendaraan)
                listkendaraan.clear_rows()
            else:
                clearcmd()
                break
        elif pilih == 2:
            clearcmd()
            print(listaksirental)
            pilih = int(input("Masukkan Aksi | "))
            if pilih == 1:
                clearcmd()
                nik = input("Masukkan NIK Peminjam: ")
                cursor.execute("select NIK, NAMA_PEMINJAM from peminjam where NIK = %s", (nik,))
                result = cursor.fetchone()
                if result:
                    data.field_names = ["NIK", "NAMA"]
                    data.add_row([result[0], result[1]])
                    print(data)
                    data.clear()

            elif pilih == 2:
                clearcmd()
                listrental.field_names = ["ID Rental", "ID Pegawai", "ID Kendaraan", "NIK Peminjam",
                                          "Tanggal Rental", "Status Rental"]
                cursor.execute("select * from rental")
                result = cursor.fetchall()
                for i in range(len(result)):
                    listrental.add_row(result[i])
                print(listrental)
                listrental.clear_rows()
        elif pilih == 4:
            clearcmd()
            logout()
        else:
            print("Aksi Tidak Valid")
            print()
            time.sleep(2)
            clearcmd()


if __name__ == '__main__':
    login_status = None
    username = None
    main()
