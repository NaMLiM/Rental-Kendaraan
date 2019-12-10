import datetime

from prettytable import PrettyTable

from init import *


def login():
    global login_status, id_pegawai, nama_pegawai
    print()
    while True:
        if login_status is None:
            print("==========Login==========")
            username = input("Masukkan Username: ")
            password = input("Masukkan Password: ")
            cursor.execute("select * from pegawai where username=%s and password=%s", (username, password))
            nama_pegawai = cursor.fetchone()[1]
            animated_loading("Login", random.uniform(0.3, 0.5))
            if cursor.fetchone():
                login_status = "Logged In"
                id_pegawai = cursor.fetchone()[0]
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
    print("Selamat Datang", nama_pegawai)


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
    listaksirental.add_row(["2.Pengembalian"])
    listaksirental.add_row(["3.List Rental"])
    listaksirental.add_row(["4.Kembali"])

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
            listrental.field_names = ["ID Rental", "ID Pegawai", "ID Kendaraan", "NIK Peminjam",
                                      "Tanggal Rental", "Status Rental"]
            cursor.execute("select * from rental")
            result = cursor.fetchall()
            for i in range(len(result)):
                listrental.add_row(result[i])
            print(listaksirental)
            pilih = int(input("Masukkan Aksi | "))
            if pilih == 1:
                clearcmd()
                nik = input("Masukkan NIK Peminjam: ")
                cursor.execute("select NIK, NAMA_PEMINJAM from peminjam where NIK = %s", (nik,))
                if cursor.fetchone():
                    data.field_names = ["NIK", "NAMA"]
                    data.add_row([cursor.fetchone()[0], cursor.fetchone()[1]])
                    print(data)
                    data.clear()
                    cursor.execute("select * from kendaraan")
                    result = cursor.fetchall()
                    for i in range(len(result)):
                        listkendaraan.add_row(result[i])
                    print(listkendaraan)
                    listkendaraan.clear_rows()
                    id_kendaraan = input("Masukkan ID Kendaraan: ")
                    cursor.execute("select ID_KENDARAAN, JUMLAH_KENDARAAN from kendaraan where ID_KENDARAAN=%s",
                                   (id_kendaraan,))
                    if cursor.fetchone():
                        jumlah_kendaraan = int(cursor.fetchone()[1])
                        if jumlah_kendaraan > 0:
                            dt = datetime.datetime.now()
                            cursor.execute("insert into "
                                           "rental(ID_PEGAWAI, ID_KENDARAAN, NIK, TANGGAL_RENTAL, STATUS_RENTAL) "
                                           "values(%s, %s, %s, %s, %s", (id_kendaraan, id_kendaraan, nik,
                                                                         dt.strftime("%Y-%m-%d %H:%M:%S"), "Meminjam"))
                            jumlah_kendaraan -= 1
                            cursor.execute("update kendaraan set JUMLAH_KENDARAAN = %s", (jumlah_kendaraan,))
                            db.commit()
                            print("SYS: Sukses Menambahkan Data!")
                        else:
                            print("SYS: Kendaraan {} Sedang Dipinjam Semua!".format(id_kendaraan))
                    else:
                        print("SYS: ID Kendaraan Tidak Ditemukan!")
                        break
            elif pilih == 2:
                clearcmd()
                print(listrental)
                id_rental = int(input("Masukkan ID Rental: "))
                cursor.execute("select ID_RENTAL, NIK, ID_KENDARAAN from rental where ID_RENTAL=%s", (id_rental,))
                if cursor.fetchone():
                    nik = cursor.fetchone()[1]
                    id_kendaraan = cursor.fetchone()[2]
                    cursor.execute("select NAMA_PEMINJAM from peminjam where NIK=%s", (nik,))
                    nama_peminjam = cursor.fetchone()[0]
                    cursor.execute("select NAMA_KENDARAAN from kendaraan where ID_KENDARAAN=%s", (id_kendaraan,))
                    nama_kendaraan = cursor.fetchone()[0]
                    data.field_names = ["SYS: Apakah {}[{}] Telah Mengembalikan Kendaraan {} ?".format(nik,
                                                                                                       nama_peminjam,
                                                                                                       nama_kendaraan)]
                    data.add_row(["1.Yes"])
                    data.add_row(["2.No"])
                    pilih = int(input("Masukkan Aksi | "))
                    if pilih == 1:
                        try:
                            cursor.execute("update rental set STATUS_RENTAL = %s where ID_RENTAL = %s", ("Kembali",
                                                                                                         id_rental))
                            cursor.execute("select JUMLAH_KENDARAAN from kendaraan where ID_KENDARAAN = %s",
                                           (id_kendaraan,))
                            jumlah_kendaraan = int(cursor.fetchone()[0])
                            jumlah_kendaraan += 1
                            cursor.execute("update kendaraan set JUMLAH_KENDARAAN = %s where ID_KENDARAAN = %s",
                                           (jumlah_kendaraan, id_kendaraan))
                            db.commit()
                            print("SYS: Pengembalian Sukses!")
                        except mysql.errors.DatabaseError:
                            print("SYS: Pengembalian Gagal!")
                listrental.clear_rows()
            elif pilih == 3:
                clearcmd()
                print(listrental)
                listrental.clear_rows()
        elif pilih == 4:
            clearcmd()
            logout()
        else:
            print("SYS: Aksi Tidak Valid")
            print()
            time.sleep(2)
            clearcmd()


if __name__ == '__main__':
    login_status = None
    main()
