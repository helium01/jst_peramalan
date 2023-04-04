import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry

# import coba as cb
import model
import jst


# Fungsi untuk menyimpan data ke dalam database
def save_data():
    # Membuat koneksi ke database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kecerdasan_buatan"
    )

    # Mendapatkan nilai dari input fields
    lokasi = lokasi_entry.get_date()
    jumblah_penjualan = jumblah_penjualan_entry.get()
    tanggal = tanggal_entry.get()
    jenis = jenis_entry.get()

    # Menyimpan data ke dalam tabel
    cursor = mydb.cursor()
    query = "INSERT INTO penjualan (bulan, motor, mobil, truk) VALUES (%s, %s, %s, %s)"
    values = (lokasi, jumblah_penjualan, tanggal, jenis)
    cursor.execute(query, values)

    # Commit perubahan dan tutup koneksi
    mydb.commit()
    mydb.close()

    # Menghapus nilai dari input fields
    lokasi_entry.delete(0, tk.END)
    jumblah_penjualan_entry.delete(0, tk.END)
    tanggal_entry.delete(0, tk.END)
    jenis_entry.delete(0, tk.END)


# def data():
#     jumblah_peramalan_label.config(text=cb.pred_uc.predicted_mean.head(1))

# Membuat GUI
root = tk.Tk()
root.title("Input Data Penjualan")



# Membuat label dan input field untuk lokasi
lokasi_label = tk.Label(root, text="tanggal")
lokasi_label.grid(row=0, column=0, padx=5, pady=5)
lokasi_entry = DateEntry(root, width=12, background='darkblue',
                      foreground='white', borderwidth=2)
lokasi_entry.grid(row=0, column=1, padx=5, pady=5)

# Membuat label dan input field untuk jumblah penjualan
jumblah_penjualan_label = tk.Label(root, text="motor")
jumblah_penjualan_label.grid(row=1, column=0, padx=5, pady=5)
jumblah_penjualan_entry = tk.Entry(root)
jumblah_penjualan_entry.grid(row=1, column=1, padx=5, pady=5)

# Membuat label dan input field untuk tanggal
tanggal_label = tk.Label(root, text="mobil")
tanggal_label.grid(row=2, column=0, padx=5, pady=5)
tanggal_entry = tk.Entry(root)
tanggal_entry.grid(row=2, column=1, padx=5, pady=5)

# Membuat label dan input field untuk jenis
jenis_label = tk.Label(root, text="truk")
jenis_label.grid(row=3, column=0, padx=5, pady=5)
jenis_entry = tk.Entry(root)
jenis_entry.grid(row=3, column=1, padx=5, pady=5)

# Membuat tombol "Simpan"
save_button = tk.Button(root, text="Simpan", command=save_data)
save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

model_button = tk.Button(root, text="latih_model", command=lambda :model.grafik())
model_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
# jumblah_peramalan_label = tk.Label(root, text="Jumlah Penjualan")
# jumblah_peramalan_label.grid(row=5, column=3, padx=5, pady=5)

ramal_button = tk.Button(root, text="lihat grafik", command=lambda:jst.grafik())
ramal_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

def open_new_form():
    # Membuat objek form baru
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="kecerdasan_buatan"
    )

    # Buat cursor untuk menjalankan query
    cursor = connection.cursor()

    # Jalankan query untuk mengambil data dari tabel MySQL
    cursor.execute("SELECT * FROM `penjualan` ORDER BY `penjualan`.`bulan` DESC ")

    # Simpan hasil query dalam variabel data
    data = cursor.fetchall()

    # Buat objek Tkinter
    root = tk.Toplevel()
    root.title("data penjualan")
    # Buat objek Frame untuk menampung elemen-elemen tabel
    frame = ttk.Frame(root)
    frame.pack()

    # Buat tabel Tkinter dengan menggunakan modul ttk
    table = ttk.Treeview(frame, columns=("motor", "mobil", "bulan", "truk"), show="headings")

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
# Membuat elemen button untuk membuka form baru
button = tk.Button(root, text="Buka data penjualan", command=open_new_form)
button.grid(row=4, column=4, columnspan=2, padx=5, pady=5)

def open_data_normalisasi():
    new_form=tk.Toplevel()
    new_form.title("data normalisasi")
    tree = ttk.Treeview(new_form)

    # Menambahkan kolom-kolom ke dalam Treeview
    tree['columns'] = ( 'motor', 'mobil', 'truk')
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('motor', width=300, anchor=tk.CENTER)
    tree.column('mobil', width=300, anchor=tk.CENTER)
    tree.column('truk', width=300, anchor=tk.CENTER)

    # Menampilkan nama kolom pada header tabel
    tree.heading('#0', text='')
    tree.heading('motor', text='motor')
    tree.heading('mobil', text='mobil')
    tree.heading('truk', text='truk')

    # Menambahkan data ke dalam Treeview
    for row in model.df_norm:
        tree.insert('', tk.END, text='', values=row)

    # Menampilkan Treeview di dalam window
    tree.pack()
    # Membuat objek form baru

button_norm = tk.Button(root, text="Buka data mormalisasi", command=lambda:open_data_normalisasi())
button_norm.grid(row=5, column=4, columnspan=2, padx=5, pady=5)

def open_data_prediksi():
    new_form=tk.Toplevel()
    new_form.title("data prediksi")
    tree = ttk.Treeview(new_form)

    # Menambahkan kolom-kolom ke dalam Treeview
    tree['columns'] = ('bulan','','motor', 'mobil', 'truk')
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('bulan', width=300, anchor=tk.CENTER)
    tree.column('', width=10, anchor=tk.CENTER)
    tree.column('motor', width=300, anchor=tk.CENTER)
    tree.column('mobil', width=300, anchor=tk.CENTER)
    tree.column('truk', width=300, anchor=tk.CENTER)

    # Menampilkan nama kolom pada header tabel
    tree.heading('#0', text='')
    tree.heading('bulan', text='bulan')
    tree.heading('', text='')
    tree.heading('motor', text='motor')
    tree.heading('mobil', text='mobil')
    tree.heading('truk', text='truk')

    # Menambahkan data ke dalam Treeview
    for row in jst.data_hasil_prediksi_tanggal:
        tree.insert('', tk.END, text='', values=row)

    # Menampilkan Treeview di dalam window
    tree.pack()
    # Membuat objek form baru

button_norm = tk.Button(root, text="Buka data prediksi", command=lambda:open_data_prediksi())
button_norm.grid(row=6, column=4, columnspan=2, padx=5, pady=5)


root.mainloop()
