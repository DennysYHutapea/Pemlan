from customtkinter import *
import tkinter
import mysql.connector
from prettytable import PrettyTable
import sys

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

def show_databases(conn):
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    return cursor.fetchall()

def list_tables(conn, database):
    cursor = conn.cursor()
    cursor.execute(f"USE {database}")
    cursor.execute("SHOW TABLES")
    return [table[0] for table in cursor.fetchall()]

def create_database(conn, database_name):
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
    conn.commit()

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("SQL Interpreter - Login")
        self.master.geometry("500x400")
        self.master.minsize(500, 400)

        self.create_widgets()

    def create_widgets(self):
        # Create a label for the login textbox
        self.login_label = CTkLabel(master=self.master, text="Username:")
        self.login_label.place(relx=0.3, rely=0.4, anchor="center")

        # Create the login textbox
        self.login_entry = CTkEntry(master=self.master)
        self.login_entry.place(relx=0.512, rely=0.4, anchor="center")

        # Create a label for the password textbox
        self.password_label = CTkLabel(master=self.master, text="Password:")
        self.password_label.place(relx=0.3, rely=0.5, anchor="center")

        # Create the password textbox (use show="*" to hide the entered characters)
        self.password_entry = CTkEntry(master=self.master, show="*")
        self.password_entry.place(relx=0.512, rely=0.5, anchor="center")

        # Create the login button with a command to trigger the login function
        self.login_button = CTkButton(
            master=self.master,
            text="Login",
            command=self.login,
            corner_radius=32,
            fg_color="#C850C0"
        )
        self.login_button.place(relx=0.5, rely=0.6, anchor="center")

        # Create a label for displaying the error message
        self.error_label = CTkLabel(master=self.master, text="")
        self.error_label.place(relx=0.5, rely=0.7, anchor="center")

    def login(self):
        username = self.login_entry.get()
        password = self.password_entry.get()

        conn = connect_to_mysql(username, password)

        if conn:
            # Successful login, open the main application window
            self.master.destroy()
            app = App()
            app.set_credentials(username, password)
        else:
            # Display a "Failed Login" message
            self.error_label.configure(text="Username atau Password Invalid", text_color="red")

class App:
    def __init__(self):
        self.master = CTk()
        self.master.title("SQL Interpreter")
        self.master.geometry("500x400")
        self.master.minsize(500, 400)

        self.username = None
        self.password = None

        self.login_window = None

        self.create_widgets()  # Call the method to create buttons

        self.master.mainloop()  # Start the main event loop

    def set_credentials(self, username, password):
        self.username = username
        self.password = password

    def set_login_window(self, login_window):
        # Store the LoginWindow instance
        self.login_window = login_window

    def create_widgets(self):
        # create 2x2 grid system
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure((0,1), weight=1)
        self.master.grid_rowconfigure(2, weight=1)

        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)


        self.result = CTkTextbox(master=self.master)
        self.result.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")

        self.combobox = CTkComboBox(master=self.master, values=[
            "Pilih",
            "Pilih basis data untuk melihat isinya",
            "Tambah basis data baru",
            "Hapus basis data",
            "Tambah data ke tabel",
            "Tampilkan data dari tabel",
            "Ubah nama database",
            "Ubah nama kolom di tabel",
            "Jadikan kolom pertama sebagai primary key",
            "Menyimpan Data yang Sudah Ada",
            "Keluar"
            ])
        self.combobox.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        self.button = CTkButton(master=self.master, command=self.button_callback, text="Pilih")
        self.button.grid(row=2, column=1, padx=20, pady=20, sticky="ew")

        self.choselist = CTkEntry(master=self.master, placeholder_text="")
        self.choselist.grid(row=0, column=0, padx=20, pady=0, sticky="ew")

        self.chosebutton = CTkButton(master=self.master, command=self.button_callback, text="Masukkan")
        self.chosebutton.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

    def button_callback(self):
        conn = connect_to_mysql("root", "password")
        if not conn:
            return

        databases = show_databases(conn)
        pilihan = list(range(1, len(databases) + 1))

        selected_value = self.combobox.get()
        inserted_value = self.choselist.get()

        if selected_value == "Pilih":
            self.result.delete("1.0", "end")  # Clear previous content

        if selected_value == "Pilih basis data untuk melihat isinya":
            self.result.configure(state="normal")

            self.result.delete("1.0", "end")  # Clear previous content

            # Loop through the databases and insert them into the text widget
            for i, db in enumerate(databases, start=1):
                text = f"{i}. {db[0]}\n"
                self.result.insert("insert", text+ "\n")
            
            if inserted_value !="":
                self.result.configure(state="normal")
                self.result.delete("1.0", "end")  # Clear previous content
                try:
                    db_choice = int(inserted_value)

                    database = databases[db_choice - 1][0]
                    tables = list_tables(conn, database)

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

                    table_string = str(table_obj)

                    # Insert the table string into the CTkTextbox
                    self.result.insert("end", table_string)

                except ValueError:
                    self.result.insert("insert", "Pilihan harus berupa angka."+ "\n")

            self.result.configure(state="disabled")

        if selected_value == "Tambah basis data baru":
            self.result.configure(state="normal")

            self.result.delete("1.0", "end")  # Clear previous content
            self.result.insert("insert", "Masukkan nama basis data baru"+ "\n")

            if inserted_value != "":
                nama_database = self.choselist.get()
                create_database(conn, nama_database)

            self.result.configure(state="disabled")

        if selected_value == "Hapus basis data":
            self.result.configure(state="normal")

            self.result.delete("1.0", "end")  # Clear previous content
            self.result.insert("insert", "Masukkan nama basis data yang akan dihapus"+ "\n")
            
            delete_database = inserted_value

            if inserted_value != "":
                cursor = conn.cursor()
                cursor.execute(f"DROP DATABASE IF EXISTS {delete_database}")
                conn.commit()
            
            self.result.configure(state="disabled")
        
        elif selected_value == "Tambah data ke tabel":
            self.result.configure(state="normal")

            self.result.delete("1.0", "end")  # Clear previous content
            self.result.insert("insert", selected_value+ "\n")

            self.result.configure(state="disabled")

        elif selected_value == "Tampilkan data dari tabel":
            self.result.configure(state="normal")

            self.result.delete("1.0", "end")  # Clear previous content
            self.result.insert("insert", selected_value+ "\n")

            self.result.configure(state="disabled")

        elif selected_value == "Ubah nama database":
            self.result.configure(state="normal")

            self.result.delete("1.0", "end")  # Clear previous content
            self.result.insert("insert", selected_value+ "\n")

            self.result.configure(state="disabled")

        elif selected_value == "Ubah nama kolom di tabel":
            self.result.configure(state="normal")

            self.result.delete("1.0", "end")  # Clear previous content
            self.result.insert("insert", selected_value+ "\n")

            self.result.configure(state="disabled")

        elif selected_value == "Jadikan kolom pertama sebagai primary key":
            self.result.configure(state="normal")

            self.result.delete("1.0", "end")  # Clear previous content
            self.result.insert("insert", selected_value+ "\n")

            self.result.configure(state="disabled")

        elif selected_value == "Menyimpan Data yang Sudah Ada":
            self.result.configure(state="normal")

            self.result.delete("1.0", "end")  # Clear previous content
            self.result.insert("insert", selected_value+ "\n")

            self.result.configure(state="disabled")

        elif selected_value == "Keluar":
            self.master.destroy()

    def result_data(self):
        pass

if __name__ == "__main__":
    root = CTk()
    login_window = LoginWindow(root)
    root.mainloop()
