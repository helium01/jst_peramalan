import tkinter as tk
from tkinter import filedialog
import mysql.connector
from mysql.connector import errorcode
import csv

# Create a GUI window
root = tk.Tk()
root.withdraw()

# Ask user to select CSV file
file_path = filedialog.askopenfilename()

# Connect to MySQL database
try:
    cnx = mysql.connector.connect(user='root', password='',
                                  host='3306', database='kecerdasan_buatan')
    cursor = cnx.cursor()

    # Read CSV file
    with open(file_path, 'r') as csvfile:
        csv_data = csv.reader(csvfile)
        header = next(csv_data)  # skip header row
        for row in csv_data:
            # Insert data into MySQL database
            add_data = ("INSERT INTO penjalan "
                        "(motor, bulan, mobil, truk) "
                        "VALUES (%s, %s, %s)")
            data = (row[0], row[1], row[2])  # assuming 3 columns in CSV file
            cursor.execute(add_data, data)

    cnx.commit()
    cursor.close()
    cnx.close()

    print("Data uploaded successfully")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
