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
            result = cursor.fetchone()
            animated_loading("Login", random.uniform(0.3, 0.5))
            if result:
                login_status = "Logged In"
                id_pegawai = result['ID_PEGAWAI']
                nama_pegawai = result['NAMA_PEGAWAI']
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
    time.sleep(2)
    clearcmd()


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
    listkendaraan.title = "List Kendaraan"
    listkendaraan.field_names = ["ID", "Nama Kendaraan", "Merk Kendaraan", "Jenis Kendaraan", "Jumlah Kendaraan"]

    listrental = PrettyTable()
    listrental.title = "List Rental"
    listrental.field_names = ["ID Rental", "ID Pegawai", "ID Kendaraan", "NIK Peminjam", "Tanggal Rental",
                              "Status Rental"]

    listpeminjam = PrettyTable()
    listpeminjam.title = "List Peminjam"
    listpeminjam.field_names = ["NIK", "Nama Peminjam", "Alamat Peminjam", "Tanggal Daftar"]

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
        data = PrettyTable()
        data.title = "Data"
        print(listaksi)
        pilih = int(input("Masukkan Aksi | "))
        if pilih == 1:
            clearcmd()
            print(listaksikendaraan)
            pilih = int(input("Masukkan Aksi | "))
            if pilih == 1:
                clearcmd()
                cursor.execute("select * from kendaraan")
                result = cursor.fetchall()
                for i in result:
                    listkendaraan.add_row([i['ID_KENDARAAN'], i['NAMA_KENDARAAN'], i['MERK_KENDARAAN'],
                                           i['JENIS_KENDARAAN'], i['JUMLAH_KENDARAAN']])
                print(listkendaraan)
                listkendaraan.clear_rows()
                input("Tekan Enter untuk melanjukan...")
                clearcmd()
            else:
                clearcmd()
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
                    data.add_row([result['NIK'], result['NAMA_PEMINJAM']])
                    print(data)
                    data.clear()
                    cursor.execute("select * from kendaraan")
                    result = cursor.fetchall()
                    for i in result:
                        listkendaraan.add_row([i['ID_KENDARAAN'], i['NAMA_KENDARAAN'], i['MERK_KENDARAAN'],
                                               i['JENIS_KENDARAAN'], i['JUMLAH_KENDARAAN']])
                    print(listkendaraan)
                    listkendaraan.clear_rows()
                    id_kendaraan = input("Masukkan ID Kendaraan: ")
                    cursor.execute("select ID_KENDARAAN, JUMLAH_KENDARAAN from kendaraan where ID_KENDARAAN=%s",
                                   (id_kendaraan,))
                    result = cursor.fetchone()
                    if result:
                        jumlah_kendaraan = int(result['JUMLAH_KENDARAAN'])
                        if jumlah_kendaraan > 0:
                            cursor.execute("insert into "
                                           "rental(ID_PEGAWAI, ID_KENDARAAN, NIK, TANGGAL_RENTAL, STATUS_RENTAL) "
                                           "values(%s, %s, %s, CURRENT_TIMESTAMP(), 'Meminjam')",
                                           (id_pegawai, id_kendaraan, nik))
                            db.commit()
                            jumlah_kendaraan -= 1
                            cursor.execute("update kendaraan set JUMLAH_KENDARAAN = %s where ID_KENDARAAN=%s",
                                           (jumlah_kendaraan, id_kendaraan))
                            db.commit()
                            print("SYS: Sukses Menambahkan Data!")
                            time.sleep(2)
                            clearcmd()
                        else:
                            print("SYS: Kendaraan {} Sedang Dipinjam Semua!".format(id_kendaraan))
                            time.sleep(2)
                            clearcmd()
                    else:
                        print("SYS: ID Kendaraan Tidak Ditemukan!")
                        time.sleep(2)
                        clearcmd()
                else:
                    clearcmd()
                    print("SYS: NIK Tidak Ditemukan!")
                    time.sleep(2)
                    clearcmd()
            elif pilih == 2:
                clearcmd()
                cursor.execute("select * from rental where STATUS_RENTAL='Meminjam'")
                result = cursor.fetchall()
                for i in result:
                    listrental.add_row(
                        [i['ID_RENTAL'], i['ID_PEGAWAI'], i['ID_KENDARAAN'], i['NIK'], i['TANGGAL_RENTAL'],
                         i['STATUS_RENTAL']])
                if result:
                    print(listrental)
                    id_rental = int(input("Masukkan ID Rental: "))
                    clearcmd()
                    cursor.execute("select ID_RENTAL, ID_KENDARAAN, NIK from rental where ID_RENTAL=%s and"
                                   " STATUS_RENTAL='Meminjam'", (id_rental,))
                    result = cursor.fetchone()
                    if result:
                        nik = result['NIK']
                        id_kendaraan = result['ID_KENDARAAN']
                        cursor.execute("select NAMA_PEMINJAM from peminjam where NIK=%s", (nik,))
                        result = cursor.fetchone()
                        nama_peminjam = result['NAMA_PEMINJAM']
                        cursor.execute("select NAMA_KENDARAAN from kendaraan where ID_KENDARAAN=%s", (id_kendaraan,))
                        result = cursor.fetchone()
                        nama_kendaraan = result['NAMA_KENDARAAN']
                        data.field_names = ["SYS: Apakah {}[{}] Telah Mengembalikan Kendaraan {} ?".format
                                            (nik, nama_peminjam, nama_kendaraan)]
                        data.add_row(["1.Yes"])
                        data.add_row(["2.No"])
                        print(data)
                        pilih = int(input("Masukkan Aksi | "))
                        if pilih == 1:
                            try:
                                cursor.execute("update rental set STATUS_RENTAL = %s where ID_RENTAL = %s", ("Kembali",
                                                                                                             id_rental))
                                db.commit()
                                cursor.execute("select JUMLAH_KENDARAAN from kendaraan where ID_KENDARAAN = %s",
                                               (id_kendaraan,))
                                result = cursor.fetchone()
                                jumlah_kendaraan = int(result['JUMLAH_KENDARAAN'])
                                jumlah_kendaraan += 1
                                cursor.execute("update kendaraan set JUMLAH_KENDARAAN = %s where ID_KENDARAAN = %s",
                                               (jumlah_kendaraan, id_kendaraan))
                                db.commit()
                                print("SYS: Pengembalian Sukses!")
                                time.sleep(2)
                                clearcmd()
                            except mysql.errors.DatabaseError:
                                print("SYS: Pengembalian Gagal!")
                                time.sleep(2)
                                clearcmd()
                        else:
                            print("SYS: Batal Mengembalikan!")
                            time.sleep(2)
                            clearcmd()
                    else:
                        print("SYS: ID Rental [{}] Tidak Ditemukan/Sudah Kembali!".format(id_rental))
                        time.sleep(2)
                        clearcmd()
                else:
                    print("SYS: Tidak Ada Yang Meminjam!")
                    time.sleep(2)
                    clearcmd()
            elif pilih == 3:
                clearcmd()
                cursor.execute("select * from rental")
                result = cursor.fetchall()
                for i in result:
                    listrental.add_row(
                        [i['ID_RENTAL'], i['ID_PEGAWAI'], i['ID_KENDARAAN'], i['NIK'], i['TANGGAL_RENTAL'],
                         i['STATUS_RENTAL']])
                print(listrental)
                input("Tekan Enter untuk melanjutkan...")
                clearcmd()
            else:
                clearcmd()
            listrental.clear_rows()
        elif pilih == 3:
            clearcmd()
            cursor.execute("select * from peminjam")
            result = cursor.fetchall()
            for i in result:
                listpeminjam.add_row([i['NIK'], i['NAMA_PEMINJAM'], i['ALAMAT_PEMINJAM'], i['TGL_DAFTAR']])
            print(listaksipeminjam)
            pilih = int(input("Masukkan Aksi | "))
            if pilih == 1:
                clearcmd()
                nik = int(input("Masukkan NIK: "))
                nama_peminjam = input("Masukkan Nama: ")
                alamat_peminjam = input("Masukkan Alamat: ")
                cursor.execute("select * from peminjam")
                result = cursor.fetchall()
                if nik not in result:
                    cursor.execute("insert into peminjam(NIK, NAMA_PEMINJAM, ALAMAT_PEMINJAM, TGL_DAFTAR) values "
                                   "(%s, %s, %s, CURRENT_TIMESTAMP())", (nik, nama_peminjam, alamat_peminjam))
                    db.commit()
                    print("SYS: Sukses!")
                    time.sleep(2)
                    clearcmd()
                else:
                    print("SYS: NIK [{}] Sudah Terdaftar!".format(nik))
                    time.sleep(2)
                    clearcmd()
            elif pilih == 2:
                clearcmd()
                print(listpeminjam)
                input("Tekan Enter untuk melanjutkan...")
                clearcmd()
            else:
                clearcmd()
            listpeminjam.clear_rows()
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
