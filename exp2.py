import tkinter as tk
from tkinter import ttk
import mysql.connector
from prettytable import PrettyTable
import csv

# Global variable to track whether the main menu is displayed
main_menu_displayed = False

# Global variable for database connection
conn = None

# Global variable for current database
current_database = None

# Function to show the main menu using GUI
def show_main_menu():
    global main_menu_displayed, current_database
    main_menu_displayed = True

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

    # Create a button to capture the user's choice
    submit_button = ttk.Button(root, text="Pilih operasi", command=lambda: process_choice(input_entry.get()))
    submit_button.pack()

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

def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="0225400405",
        )
        if conn.is_connected():
            print("....Koneksi ke MySQL dimulai...")
            return conn
    except mysql.connector.Error as err:
        print(f"Kesalahan koneksi ke MySQL: {err}")
    return None

# Function to process the user's choice
def process_choice(choice):
    databases = None

    if choice == "1":
        db_choice = input("Pilih basis data yang ingin dilihat isinya ({})".format(", ".join(map(str, pilihan))))
        try:
            db_choice = int(db_choice)
            if db_choice not in pilihan:
                print("Pilihan tidak valid.")
            database = databases[db_choice - 1][0]
            tables = gui_list_tables(conn, database)
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
        # Implement the logic for option 2 (Tambah basis data baru) here
        pass
    elif choice == "3":
        # Implement the logic for option 3 (Hapus basis data) here
        pass
    elif choice == "4":
        # Implement the logic for option 4 (Tambah data ke tabel) here
        pass
    elif choice == "5":
        # Implement the logic for option 5 (Tampilkan data dari tabel) here
        pass
    elif choice == "6":
        # Implement the logic for option 6 (Ubah nama database) here
        pass
    elif choice == "7":
        # Implement the logic for option 7 (Ubah nama kolom di tabel) here
        pass
    elif choice == "8":
        # Implement the logic for option 8 (Jadikan kolom pertama sebagai primary key) here
        pass
    elif choice == "9":
        # Implement the logic for option 9 (Menyimpan Data yang Sudah Ada) here
        pass
    elif choice == "10":
        quit_program()  # Call the function to exit the program

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
    tables = gui_list_tables(database)
    for i, table in enumerate(tables, start=1):
        table_button = ttk.Button(table_selection_frame, text=table, command=lambda table=table: show_table_data(database, table))
        table_button.grid(row=i, column=0, padx=10, pady=5)

    current_database = database

# Function to exit the program gracefully
def quit_program():
    global main_menu_displayed  # Access the global variable
    main_menu_displayed = False
    root.quit()  # Exit the Tkinter main loop

# Define the main window
root = tk.Tk()
root.title("MySQL Database Manager")

# Start by showing the main menu using GUI
show_main_menu()

# Start the Tkinter main loop
root.mainloop()
