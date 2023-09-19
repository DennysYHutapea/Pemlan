import mysql.connector

# Mapping tipe data MySQL ke deskripsi yang lebih dimengerti
type_mapping = {
    "INT": "bilangan bulat",
    "VARCHAR": "teks",
    # Tambahkan tipe data lain sesuai kebutuhan Anda
}

# Define the column types for your tables here
table_column_types = {
    "table1": {
        "column1": "bilangan bulat",
        "column2": "teks",
    },
    # Define column types for other tables as needed
}

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="020874",
)

# Check if the connection is successful
if conn.is_connected():
    print("....Koneksi ke MySQL dimulai...")

    while True:
        # Get the cursor object
        cursor = conn.cursor()

        # Execute the `SHOW DATABASES` query
        cursor.execute("SHOW DATABASES")

        # Get the list of databases
        databases = cursor.fetchall()

        # Print the list of databases
        print("\nDaftar Basis Data:")
        for i, db in enumerate(databases, start=1):
            print(f"{i}. {db[0]}")

        # Buat list pilihan
        pilihan = list(range(1, len(databases) + 1))

        # Minta user memilih basis data atau operasi
        print("\nPilihan:")
        print("1. Pilih basis data untuk melihat isinya.")
        print("2. Tambah basis data baru.")
        print("3. Hapus basis data.")
        print("4. Tambah data ke tabel.")
        print("5. Tampilkan data dari tabel.")
        print("6. Keluar.")
        choice = input("Pilih operasi (1/2/3/4/5/6): ")

        if choice == "1":
            # Minta user memilih basis data
            db_choice = input("Pilih basis data yang ingin dilihat ({}): ".format(", ".join(map(str, pilihan))))            
            try:
                db_choice = int(db_choice)
                if db_choice not in pilihan:
                    print("Pilihan tidak valid.")
                    continue
                database = databases[db_choice - 1][0]
            except ValueError:
                print("Pilihan harus berupa angka.")
                continue

            # Lihat isi dari basis data yang dipilih
            cursor.execute("USE {}".format(database))
            cursor.execute("SHOW TABLES")

            tables = cursor.fetchall()

            print("\nIsi database {}:".format(database))
            for table in tables:
                cursor.execute("SELECT * FROM {}".format(table[0]))

                rows = cursor.fetchall()

                for row in rows:
                    print(row)

            # Tampilkan pesan keterangan ketika kembali ke halaman awal
            print("\nKembali ke halaman awal...")

        elif choice == "2":
            # Minta user untuk nama basis data baru
            new_database = input("Masukkan nama basis data baru: ")

            # Buat basis data baru jika belum ada
            cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(new_database))
            print("Basis data '{}' berhasil ditambahkan.".format(new_database))

            # Commit perubahan untuk membuat basis data baru
            conn.commit()

            # Minta user untuk membuat tabel di basis data baru
            create_table = input("Buat tabel di basis data '{}'? (y/n): ".format(new_database))

            if create_table.lower() == 'y':
                # Menampilkan pilihan sintaks SQL untuk membuat tabel
                print("Pilihan Sintaks SQL untuk Membuat Tabel:")
                print("1. Membuat tabel dengan kolom bilangan bulat dan teks")
                print("2. Membuat tabel dengan kolom bilangan bulat, teks, dan primary key")

                table_syntax = input("Pilih sintaks yang ingin digunakan (1/2): ")

                if table_syntax == "1":
                    table_definition = """
                    CREATE TABLE table_name (
                        column1 INT,
                        column2 VARCHAR(255)
                    )
                    """
                elif table_syntax == "2":
                    table_definition = """
                    CREATE TABLE table_name (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        column1 INT,
                        column2 VARCHAR(255)
                    )
                    """
                else:
                    print("Sintaks yang dipilih tidak valid.")
                    continue

                # Mengganti 'table_name' dengan nama tabel yang diinginkan
                table_name = input("Masukkan nama tabel: ")
                table_definition = table_definition.replace("table_name", table_name)

                # Eksekusi perintah SQL untuk membuat tabel
                cursor.execute("USE {}".format(new_database))
                cursor.execute(table_definition)
                print("Tabel '{}' berhasil dibuat di basis data '{}'.".format(table_name, new_database))

                # Commit perubahan untuk membuat tabel baru
                conn.commit()

            # Tampilkan pesan keterangan ketika kembali ke halaman awal
            print("\nKembali ke halaman awal...")

        elif choice == "3":
            # Minta user untuk nama basis data yang akan dihapus
            del_database = input("Masukkan nama basis data yang akan dihapus: ")

            # Hapus basis data jika ada
            cursor.execute("DROP DATABASE IF EXISTS {}".format(del_database))
            print("Basis data '{}' berhasil dihapus.".format(del_database))

            # Commit perubahan untuk menghapus basis data
            conn.commit()

            # Tampilkan pesan keterangan ketika kembali ke halaman awal
            print("\nKembali ke halaman awal...")

        elif choice == "4":
            # Minta user memilih basis data
            db_choice = input("Pilih basis data tempat tabel berada ({})".format(", ".join(map(str, pilihan))))
            try:
                db_choice = int(db_choice)
                if db_choice not in pilihan:
                    print("Pilihan tidak valid.")
                    continue
                database = databases[db_choice - 1][0]
            except ValueError:
                print("Pilihan harus berupa angka.")
                continue

            # Minta user memilih tabel untuk menambahkan data
            cursor.execute("USE {}".format(database))
            cursor.execute("SHOW TABLES")

            tables = cursor.fetchall()

            print("\nDaftar Tabel di database {}:".format(database))
            for i, table in enumerate(tables, start=1):
                print(f"{i}. {table[0]}")

            table_choice = input("Masukkan nomor tabel tempat Anda ingin menambahkan data: ")
            try:
                table_choice = int(table_choice)
                if table_choice < 1 or table_choice > len(tables):
                    print("Nomor tabel tidak valid.")
                    continue
                table_name = tables[table_choice - 1][0]
            except ValueError:
                print("Nomor tabel harus berupa angka.")
                continue

            # Cek apakah tabel ada di basis data yang dipilih
            if table_name not in [table[0] for table in tables]:
                print("Tabel '{}' tidak ditemukan di basis data '{}'.".format(table_name, database))
                continue

            # Minta user memasukkan data ke dalam tabel
            print("Masukkan data ke dalam tabel (pisahkan dengan koma, contoh: nilai1, nilai2)")

            # Ambil definisi kolom dari tabel yang sebenarnya
            cursor.execute("DESCRIBE {}".format(table_name))
            columns = cursor.fetchall()
            column_names = [col[0] for col in columns]

            data_values = input("Data: ").split(",")

            if len(data_values) != len(column_names):
                print("Jumlah nilai yang dimasukkan tidak sesuai dengan jumlah kolom dalam tabel.")
                continue

            insert_values = []
            for i in range(len(column_names)):
                column_name = column_names[i]
                column_type = table_column_types.get(column_name, "teks")  # Menggunakan teks sebagai tipe data default
                value = data_values[i].strip()
                try:
                    if column_type.startswith("bilangan bulat"):
                        insert_values.append(int(value))
                    else:
                        insert_values.append(value)
                except ValueError:
                    print("Kesalahan: Nilai '{}' tidak sesuai dengan tipe data '{}'.".format(value, column_type))
                    continue

            # Buat query SQL untuk menambahkan data ke tabel
            placeholders = ", ".join(["%s"] * len(insert_values))
            insert_query = "INSERT INTO {} ({}) VALUES ({})".format(table_name, ", ".join(column_names), placeholders)

            try:
                # Eksekusi perintah SQL untuk menambahkan data
                cursor.execute(insert_query, insert_values)
                print("Data berhasil ditambahkan ke tabel '{}'.".format(table_name))

                # Commit perubahan untuk menambahkan data
                conn.commit()
            except mysql.connector.Error as err:
                print("Gagal menambahkan data: {}".format(err))

            # Tampilkan pesan keterangan ketika kembali ke halaman awal
            print("\nKembali ke halaman awal...")

        elif choice == "5":
            # Minta user memilih basis data
            db_choice = input("Pilih basis data tempat tabel berada ({})".format(", ".join(map(str, pilihan))))
            try:
                db_choice = int(db_choice)
                if db_choice not in pilihan:
                    print("Pilihan tidak valid.")
                    continue
                database = databases[db_choice - 1][0]
            except ValueError:
                print("Pilihan harus berupa angka.")
                continue

            # Minta user memilih tabel untuk menampilkan data
            cursor.execute("USE {}".format(database))
            cursor.execute("SHOW TABLES")

            tables = cursor.fetchall()

            print("\nDaftar Tabel di database {}:".format(database))
            for i, table in enumerate(tables, start=1):
                print(f"{i}. {table[0]}")

            table_choice = input("Masukkan nomor tabel tempat Anda ingin menampilkan data: ")
            try:
                table_choice = int(table_choice)
                if table_choice < 1 or table_choice > len(tables):
                    print("Nomor tabel tidak valid.")
                    continue
                table_name = tables[table_choice - 1][0]
            except ValueError:
                print("Nomor tabel harus berupa angka.")
                continue

            # Cek apakah tabel ada di basis data yang dipilih
            if table_name not in [table[0] for table in tables]:
                print("Tabel '{}' tidak ditemukan di basis data '{}'.".format(table_name, database))
                continue

            # Tampilkan isi dari tabel yang dipilih
            cursor.execute("SELECT * FROM {}".format(table_name))

            rows = cursor.fetchall()

            print("\nIsi tabel '{}' di basis data '{}':".format(table_name, database))
            for row in rows:
                print(row)

            # Tampilkan pesan keterangan ketika kembali ke halaman awal
            print("\nKembali ke halaman awal...")

        elif choice == "6":
            # Keluar dari loop tak terbatas
            break

        else:
            print("Operasi tidak valid.")

    print("\n....Koneksi ke MySQL ditutup.....")

    # Close the cursor and connection
    cursor.close()
    conn.close()
