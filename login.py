import tkinter as ttk
from tkinter import messagebox
import mysql.connector
from prettytable import PrettyTable
import csv

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

# Define your MySQL connection function here
def connect_to_mysql(user, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
        )
        if conn.is_connected():
            print("\n....Koneksi ke MySQL dimulai...")
            return conn
    except mysql.connector.Error as err:
        print(f"Kesalahan koneksi ke MySQL: {err}")
    return None

# Function to handle the login button click
def login():
    user = username_entry.get()
    password = password_entry.get()
    
    # Call your connect_to_mysql function
    conn = connect_to_mysql(user, password)
    
    if conn:
        # Successful login
        show_main_menu(user, password)
    else:
        messagebox.showerror("Error", "Gagal terhubung ke MySQL. Pastikan informasi login benar.")

def show_databases(conn):
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    return cursor.fetchall()

def list_tables(conn, database):
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute("SHOW TABLES")
    return [table[0] for table in cursor.fetchall()]

def list_columns(conn, database, table):
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute(f"DESCRIBE {table}")
    return [column[0] for column in cursor.fetchall()]

def create_database(conn, database_name):
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    conn.commit()
    print(f"Basis data '{database_name}' berhasil ditambahkan.")

def create_table(conn, database, table_name, table_definition):
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute(table_definition)
    conn.commit()
    print(f"Tabel '{table_name}' berhasil dibuat di basis data '{database}'.")

def insert_data(conn, database, table_name, column_names, data):
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")
    data_str = ", ".join(["'{}'".format(value) for value in data])
    insert_query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({data_str})"
    cursor.execute(insert_query)
    conn.commit()
    print("Data berhasil ditambahkan ke tabel '{}'.".format(table_name))


def rename_column(conn, database, table_name, old_column_name, new_column_name, new_column_type):
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute(f"ALTER TABLE {table_name} CHANGE COLUMN {old_column_name} {new_column_name} {new_column_type}")
    conn.commit()
    print("Nama kolom '{}' di tabel '{}' di basis data '{}' berhasil diubah menjadi '{}' dengan tipe data '{}'.".format(old_column_name, table_name, database, new_column_name, new_column_type))

def add_primary_key(conn, database, table_name, primary_key_column):
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute(f"ALTER TABLE {table_name} ADD PRIMARY KEY ({primary_key_column})")
    conn.commit()
    print("Kolom '{}' di tabel '{}' di basis data '{}' berhasil dijadikan primary key.".format(primary_key_column, table_name, database))

def save_table_to_csv(conn, database, table_name, column_names, file_name):
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    with open(file_name, "w") as csv_file:
        csv_file.write(",".join(column_names) + "\n")
        for row in rows:
            csv_file.write(",".join(map(str, row)) + "\n")
    print("Data dari tabel '{}' di basis data '{}' berhasil disimpan ke dalam file '{}'.".format(table_name, database, file_name))
    
def save_to_csv(file_name, column_names, rows):
    import csv

    with open(file_name, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)
        for row in rows:
            csv_writer.writerow(row)

    print(f"Data saved to '{file_name}' successfully.")

# Function to show a new page with additional options
def show_option_page(option):
    # Destroy the current main menu page
    main_menu_frame.destroy()
    
    # Create a new page for the selected option
    option_page_frame = ttk.Frame(root)
    option_page_frame.pack()
    
    # Display options based on the selected option
    if option == 1:
        label = ttk.Label(option_page_frame, text="Options for Option 1")
        label.pack()
        # Add more widgets for Option 1 here
    elif option == 2:
        label = ttk.Label(option_page_frame, text="Options for Option 2")
        label.pack()
        # Add more widgets for Option 2 here
    # Add more elif blocks for other options as needed

# Function to create the main menu window
def show_main_menu(username,password):
    option_page_frame = ttk.Frame(root)
    option_page_frame.pack()

    # Destroy the current option page
    option_page_frame.destroy()

    global main_menu_displayed, current_database
    main_menu_displayed = True
    main_menu_frame = ttk.Frame(root)
    main_menu_frame.pack()

    # Remove any previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create and pack labels for your menu text
    label1 = ttk.Label(root, text="....Koneksi ke MySQL dimulai...")
    label1.pack()

    label2 = ttk.Label(root, text="Daftar Basis Data:")
    label2.pack()

    # Replace the following list with your actual database list
    databases = ["basis1", "information_schema", "mysql", "performance_schema", "sys"]

    for i, db in enumerate(databases, start=1):
        db_label = ttk.Label(root, text=f"{i}. {db}")
        db_label.pack()

    label3 = ttk.Label(root, text="Pilihan:")
    label3.pack()

    label4 = ttk.Label(root, text="1. Pilih basis data untuk melihat isinya.")
    label4.pack()

    label5 = ttk.Label(root, text="2. Tambah basis data baru.")
    label5.pack()

    label6 = ttk.Label(root, text="3. Hapus basis data.")
    label6.pack()

    label7 = ttk.Label(root, text="4. Tambah data ke tabel.")
    label7.pack()

    label8 = ttk.Label(root, text="5. Tampilkan data dari tabel.")
    label8.pack()

    label9 = ttk.Label(root, text="6. Ubah nama database.")
    label9.pack()

    label10 = ttk.Label(root, text="7. Ubah nama kolom di tabel.")
    label10.pack()

    label11 = ttk.Label(root, text="8. Jadikan kolom pertama sebagai primary key.")
    label11.pack()

    label12 = ttk.Label(root, text="9. Menyimpan Data yang Sudah Ada.")
    label12.pack()

    label13 = ttk.Label(root, text="10. Keluar.")
    label13.pack()

    # Create an entry widget for user input
    input_entry = ttk.Entry(root)
    input_entry.pack()

    # Add buttons for the main menu options
    option_button = ttk.Button(root, text="Pilih operasi", command=lambda: process_choice(input_entry.get(),username,password))
    option_button.pack()

# Function to switch to the database selection screen
def show_database_selection():
    global current_database

    # Remove the previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new frame for the database selection screen
    database_selection_frame = ttk.Frame(root)
    database_selection_frame.pack()

    # Populate the frame with database options
    databases = show_databases()
    for i, db in enumerate(databases, start=1):
        db_button = ttk.Button(database_selection_frame, text=db, command=lambda db=db: show_table_selection(db))
        db_button.grid(row=i, column=0, padx=10, pady=5)

    current_database = None  # Reset current database

# Function to process the user's choice
def process_choice(choice, user, password):
    conn = connect_to_mysql(user, password)
    if not conn:
        return

    database = None  # Tambahkan inisialisasi untuk variabel database

    while True:
        databases = show_databases(conn)
        pilihan = list(range(1, len(databases) + 1))

        if choice == "1":
            db_choice = input("Pilih basis data yang ingin dilihat isinya ({})".format(", ".join(map(str, pilihan))))
            try:
                db_choice = int(db_choice)
                if db_choice not in pilihan:
                    print("Pilihan tidak valid.")
                database = databases[db_choice - 1][0]
                tables = list_tables(conn, database)
                print("\nIsi database {}:".format(database))
                for table in tables:
                    print("\nTabel '{}' di basis data '{}':".format(table, database))
                    cursor = conn.cursor()
                    cursor.execute(f"USE {database}")
                    cursor.execute(f"SELECT * FROM {table}")
                    rows = cursor.fetchall()
                    table_obj = PrettyTable()
                    table_obj.field_names = [column[0] for column in cursor.description]
                    for row in rows:
                        table_obj.add_row(row)
                    print(table_obj)
            except ValueError:
                print("Pilihan harus berupa angka.")
                
        elif choice == "2":
            new_database = input("Masukkan nama basis data baru: ")
            create_database(conn, new_database)

            create_table_option = input("Buat tabel di basis data '{}'? (y/n): ".format(new_database))
            if create_table_option.lower() == 'y':
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
                table_name = input("Masukkan nama tabel: ")
                table_definition = table_definition.replace("table_name", table_name)
                create_table(conn, new_database, table_name, table_definition)

        elif choice == "3":
            del_database = input("Masukkan nama basis data yang akan dihapus: ")
            cursor = conn.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {del_database}")
            conn.commit()
            print("Basis data '{}' berhasil dihapus.".format(del_database))
            
        elif choice == "4":
            db_choice = input("Pilih basis data tempat tabel berada ({}): ".format(", ".join(map(str, pilihan))))
            try:
                db_choice = int(db_choice)
                if db_choice not in pilihan:
                    print("Pilihan tidak valid.")
                    continue
                database = databases[db_choice - 1][0]
                tables = list_tables(conn, database)
                print("\nDaftar Tabel di Basis Data '{}'".format(database))
                for i, table in enumerate(tables, start=1):
                    print("{}. {}".format(i, table))
                table_choice = input("Pilih tabel tempat data akan ditambahkan ({})".format(", ".join(map(str, range(1, len(tables) + 1)))))
                try:
                    table_choice = int(table_choice)
                    if table_choice not in range(1, len(tables) + 1):
                        print("Pilihan tidak valid.")
                        continue
                    table_name = tables[table_choice - 1]
                    column_names = list_columns(conn, database, table_name)
                    data = []
                    print("\nMasukkan data untuk tabel '{}' di basis data '{}'".format(table_name, database))
                    for column in column_names:
                        value = input("Masukkan nilai untuk kolom '{}': ".format(column))
                        data.append(value)
                    insert_data(conn, database, table_name, column_names, data)
                except ValueError:
                    print("Pilihan harus berupa angka.")
            except ValueError:
                print("Pilihan harus berupa angka.")

        elif choice == "5":
            db_choice = input("Pilih basis data tempat tabel baru akan ditambahkan ({})".format(", ".join(map(str, pilihan))))
            try:
                db_choice = int(db_choice)
                if db_choice not in pilihan:
                    print("Pilihan tidak valid.")
                    continue
                database = databases[db_choice - 1][0]
                table_name = input("Masukkan nama tabel baru: ")
                print("Pilihan Sintaks SQL untuk Membuat Tabel:")
                print("1. Membuat tabel dengan kolom bilangan bulat dan teks")
                print("2. Membuat tabel dengan kolom bilangan bulat, teks, dan primary key")
                table_syntax = input("Pilih sintaks yang ingin digunakan (1/2): ")
                if table_syntax == "1":
                    table_definition = """
                    CREATE TABLE {} (
                        column1 INT,
                        column2 VARCHAR(255)
                    )
                    """.format(table_name)
                elif table_syntax == "2":
                    table_definition = """
                    CREATE TABLE {} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        column1 INT,
                        column2 VARCHAR(255)
                    )
                    """.format(table_name)
                else:
                    print("Sintaks yang dipilih tidak valid.")
                    continue
                create_table(conn, database, table_name, table_definition)
            except ValueError:
                print("Pilihan harus berupa angka.")

        elif choice == "6":
            db_choice = input("Pilih basis data tempat tabel berada ({})".format(", ".join(map(str, pilihan))))
            try:
                db_choice = int(db_choice)
                if db_choice not in pilihan:
                    print("Pilihan tidak valid.")
                    continue
                database = databases[db_choice - 1][0]
                tables = list_tables(conn, database)
                print("\nDaftar Tabel di Basis Data '{}'".format(database))
                for i, table in enumerate(tables, start=1):
                    print("{}. {}".format(i, table))
                table_choice = input("Pilih tabel tempat data akan ditampilkan ({})".format(", ".join(map(str, range(1, len(tables) + 1)))))
                try:
                    table_choice = int(table_choice)
                    if table_choice not in range(1, len(tables) + 1):
                        print("Pilihan tidak valid.")
                        continue
                    table_name = tables[table_choice - 1]
                    column_names = list_columns(conn, database, table_name)
                    cursor = conn.cursor()
                    cursor.execute(f"USE {database}")
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    table_obj = PrettyTable()
                    table_obj.field_names = column_names
                    for row in rows:
                        table_obj.add_row(row)
                    print("\nData dari tabel '{}' di basis data '{}':".format(table_name, database))
                    print(table_obj)
                except ValueError:
                    print("Pilihan harus berupa angka.")
            except ValueError:
                print("Pilihan harus berupa angka.")

        elif choice == "7":
            db_choice = input("Pilih basis data tempat tabel berada ({})".format(", ".join(map(str, pilihan))))
            try:
                db_choice = int(db_choice)
                if db_choice not in pilihan:
                    print("Pilihan tidak valid.")
                    continue
                database = databases[db_choice - 1][0]
                tables = list_tables(conn, database)
                print("\nDaftar Tabel di Basis Data '{}'".format(database))
                for i, table in enumerate(tables, start=1):
                    print("{}. {}".format(i, table))
                table_choice = input("Pilih tabel yang berisi kolom yang akan diubah namanya ({})".format(", ".join(map(str, range(1, len(tables) + 1)))))
                try:
                    table_choice = int(table_choice)
                    if table_choice not in range(1, len(tables) + 1):
                        print("Pilihan tidak valid.")
                        continue
                    table_name = tables[table_choice - 1]
                    column_names = list_columns(conn, database, table_name)
                    print("\nDaftar Kolom di Tabel '{}' di Basis Data '{}'".format(table_name, database))
                    for i, column in enumerate(column_names, start=1):
                        print("{}. {}".format(i, column))
                    column_choice = input("Pilih kolom yang ingin diubah namanya ({})".format(", ".join(map(str, range(1, len(column_names) + 1)))))
                    try:
                        column_choice = int(column_choice)
                        if column_choice not in range(1, len(column_names) + 1):
                            print("Pilihan tidak valid.")
                            continue
                        old_column_name = column_names[column_choice - 1]
                        new_column_name = input("Masukkan nama baru untuk kolom '{}': ".format(old_column_name))
                        print("Pilihan Tipe Data:")
                        print("1. bilangan bulat")
                        print("2. teks")
                        new_column_type_choice = input("Pilih tipe data baru untuk kolom '{}': ".format(new_column_name))
                        type_mapping = {
                            "1": "INT",
                            "2": "VARCHAR(255)",
                        }
                        new_column_type = type_mapping.get(new_column_type_choice)
                        if new_column_type is None:
                            print("Pilihan tipe data tidak valid.")
                            continue
                        rename_column(conn, database, table_name, old_column_name, new_column_name, new_column_type)
                    except ValueError:
                        print("Pilihan harus berupa angka.")
                except ValueError:
                    print("Pilihan harus berupa angka.")
            except ValueError:
                print("Pilihan harus berupa angka.")

        elif choice == "8":
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

            # Minta user memilih tabel
            cursor.execute("USE {}".format(database))
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()

            print("\nDaftar Tabel di Basis Data '{}'".format(database))
            for i, table in enumerate(tables, start=1):
                print("{}. {}".format(i, table[0]))

            table_choice = input("Pilih tabel tempat kolom pertama akan dijadikan primary key ({})".format(", ".join(map(str, range(1, len(tables) + 1)))))
            try:
                table_choice = int(table_choice)
                if table_choice not in range(1, len(tables) + 1):
                    print("Pilihan tidak valid.")
                    continue
                table_name = tables[table_choice - 1][0]
            except ValueError:
                print("Pilihan harus berupa angka.")
                continue

            # Minta user memilih kolom yang akan dijadikan primary key
            cursor.execute("DESCRIBE {}".format(table_name))
            columns = cursor.fetchall()
            column_names = [column[0] for column in columns]

            print("\nDaftar Kolom di Tabel '{}' di Basis Data '{}'".format(table_name, database))
            for i, column in enumerate(column_names, start=1):
                print("{}. {}".format(i, column))

            column_choice = input("Pilih kolom pertama yang akan dijadikan primary key ({})".format(", ".join(map(str, range(1, len(column_names) + 1)))))
            try:
                column_choice = int(column_choice)
                if column_choice not in range(1, len(column_names) + 1):
                    print("Pilihan tidak valid.")
                    continue
                primary_key_column = column_names[column_choice - 1]
            except ValueError:
                print("Pilihan harus berupa angka.")
                continue

            # Tambahkan primary key ke tabel
            cursor.execute("ALTER TABLE {} ADD PRIMARY KEY ({})".format(table_name, primary_key_column))
            print("Kolom '{}' di tabel '{}' di basis data '{}' berhasil dijadikan primary key.".format(primary_key_column, table_name, database))

            # Commit perubahan
            conn.commit()

            # Tampilkan pesan keterangan ketika kembali ke halaman awal
            print("\nKembali ke halaman awal...")

        elif choice == "9":
            db_choice = input("Pilih basis data yang ingin disimpan ({})".format(", ".join(map(str, pilihan))))
            try:
                db_choice = int(db_choice)
                if db_choice not in pilihan:
                    print("Pilihan tidak valid.")
                    continue
                database = databases[db_choice - 1][0]
                tables = list_tables(conn, database)
                print("\nDaftar Tabel di Basis Data '{}'".format(database))
                for i, table in enumerate(tables, start=1):
                    print("{}. {}".format(i, table))
                table_choice = input("Pilih tabel yang ingin disimpan ({})".format(", ".join(map(str, range(1, len(tables) + 1)))))
                try:
                    table_choice = int(table_choice)
                    if table_choice not in range(1, len(tables) + 1):
                        print("Pilihan tidak valid.")
                        continue
                    table_name = tables[table_choice - 1]
                    column_names = list_columns(conn, database, table_name)
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    file_name = input("Masukkan nama file untuk menyimpan data (format CSV): ")
                    save_to_csv(file_name, column_names, rows)
                except ValueError:
                    print("Pilihan harus berupa angka.")
            except ValueError:
                print("Pilihan harus berupa angka.")

        elif choice == "10":
            quit_program()  # Call the function to exit the program
            break

# Function to switch to the database selection screen
def show_database_selection():
    global current_database

    # Remove the previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new frame for the database selection screen
    database_selection_frame = ttk.Frame(root)
    database_selection_frame.pack()

    # Populate the frame with database options
    databases = show_databases()
    for i, db in enumerate(databases, start=1):
        db_button = ttk.Button(database_selection_frame, text=db, command=lambda db=db: show_table_selection(db))
        db_button.grid(row=i, column=0, padx=10, pady=5)

    current_database = None  # Reset current database

# Function to switch to the table selection screen
def show_table_selection(database):
    global current_database

    # Remove the previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create a new frame for the table selection screen
    table_selection_frame = ttk.Frame(root)
    table_selection_frame.pack()

    # Populate the frame with table options
    tables = list_tables(database)
    for i, table in enumerate(tables, start=1):
        table_button = ttk.Button(table_selection_frame, text=table, command=lambda table=table: show_table_data(database, table))
        table_button.grid(row=i, column=0, padx=10, pady=5)

    current_database = database

def show_table_data(database, table_name):
    # Create a new window for displaying table data
    table_window = ttk.Toplevel(root)
    table_window.title(f"Data in Table '{table_name}'")

    # Connect to the MySQL database
    conn = connect_to_mysql(username_entry.get(), password_entry.get())

    if conn:
        cursor = conn.cursor()
        cursor.execute(f"USE {database}")
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        column_names = [column[0] for column in cursor.description]

        # Create a PrettyTable to display the data
        table = PrettyTable(column_names)
        for row in rows:
            table.add_row(row)

        # Create a label to display the table data
        table_label = ttk.Label(table_window, text=str(table), justify="left")
        table_label.pack()

        # Create a button to go back to the main menu
        back_button = ttk.Button(table_window, text="Back to Main Menu", command=show_main_menu)
        back_button.pack()

    else:
        messagebox.showerror("Error", "Failed to connect to MySQL database. Please check your login information.")

# Function to exit the program gracefully
def quit_program():
    global main_menu_displayed  # Access the global variable
    main_menu_displayed = False
    root.quit()  # Exit the Tkinter main loop

# Create the main Tkinter window for login
root = ttk.Tk()
root.title("Login to MySQL")

# Create and position the username label and entry field
username_label = ttk.Label(root, text="Username:")
username_label.pack()
username_entry = ttk.Entry(root)
username_entry.pack()

# Create and position the password label and entry field
password_label = ttk.Label(root, text="Password:")
password_label.pack()
password_entry = ttk.Entry(root, show="*")  # Use show="*" to hide the password characters
password_entry.pack()

# Create and position the login button
login_button = ttk.Button(root, text="Login", command=login)
login_button.pack()

# Global variable to track whether the main menu is displayed
main_menu_displayed = False

# Global variable for database connection
conn = None

# Global variable for current database
current_database = None

# Create the main menu frame
main_menu_frame = ttk.Frame(root)
main_menu_frame.pack()

# Start the Tkinter main loop
root.mainloop()
