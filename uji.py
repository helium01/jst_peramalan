import tkinter as tk
import mysql.connector
from tkinter import ttk

# Buat koneksi ke database MySQL
connection = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="kecerdasan_buatan"
)

# Buat cursor untuk menjalankan query
cursor = connection.cursor()

# Jalankan query untuk mengambil data dari tabel MySQL
cursor.execute("SELECT * FROM penjualan")

# Simpan hasil query dalam variabel data
data = cursor.fetchall()

print(data)

# Buat objek Tkinter
root = tk.Tk()

# Buat objek Frame untuk menampung elemen-elemen tabel
frame = ttk.Frame(root)
frame.pack()

# Buat tabel Tkinter dengan menggunakan modul ttk
table = ttk.Treeview(frame, columns=("motor", "mobil", "bulan","truk"), show="headings")

# Tambahkan header tabel
table.heading("motor", text="Kolom 1")
table.heading("bulan", text="Kolom 2")
table.heading("mobil", text="Kolom 3")
table.heading("truk", text="Kolom 4")

# Tambahkan data ke dalam tabel
for row in data:
    table.insert("", "end", values=row)

# Buat grid pada tabel
for col in table["columns"]:
    table.column(col, width=100, anchor="center")
    table.heading(col, text=col, anchor="center")

# Tampilkan tabel

table.pack()

# Jalankan program
root.mainloop()
