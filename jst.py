import pandas as pd
import numpy as np
import mysql.connector
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# Mengambil data dari database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="kecerdasan_buatan"
)

query = "SELECT * FROM penjualan"
# membuat cursor
mycursor = mydb.cursor()

# melakukan query SELECT
mycursor.execute(query)
# mengambil hasil query
myresult = mycursor.fetchall()
df = pd.DataFrame(myresult, columns=['id','motor', 'bulan', 'mobil', 'truk'])
cols=['id']
df.drop(cols,axis=1,inplace=True)
# print(df)


# mengubah kolom Month menjadi tipe data datetime dan menjadikannya sebagai index
df['bulan'] = pd.to_datetime(df['bulan'])
df.set_index('bulan', inplace=True)

# memisahkan data latih dan data uji
train_data = df.iloc[:-12]
test_data = df.iloc[-12:]

# normalisasi data
scaler = MinMaxScaler()
train_data_norm = scaler.fit_transform(train_data)
test_data_norm = scaler.transform(test_data)

# mempersiapkan data latih dan data uji
X_train, y_train = train_data_norm[:, :-2], train_data_norm[:, -2:]
X_test, y_test = test_data_norm[:, :-2], test_data_norm[:, -2:]

# memuat model yang telah dilatih sebelumnya
model = tf.keras.models.load_model('model.h5')

# menggunakan model untuk memprediksi penjualan kendaraan bermotor pada data uji
y_pred_norm = model.predict(X_test)
y_pred = scaler.inverse_transform(np.hstack((X_test, y_pred_norm)))

# data_hasil_prediksi = np.column_stack((test_data.values, y_pred.reshape(-1, 1)))
data_hasil_prediksi_tanggal = np.column_stack((test_data.index.to_list(), y_pred))
print(data_hasil_prediksi_tanggal)

# membuat grafik hasil prediksi
def grafik():
    plt.figure(figsize=(10, 5))
    # plt.plot(train_data.index, train_data['mobil'], label=' data training mobil')
    # plt.plot(test_data.index, test_data['mobil'], label='data asli mobil')
    plt.plot(test_data.index, y_pred[:, 1], label='prediksi  motor')
    # plt.plot(train_data.index, train_data['motor'], label='Tdata training motor')
    # plt.plot(test_data.index, test_data['motor'], label='data asli motor')
    plt.plot(test_data.index, y_pred[:, 0], label='prediksi motor')
    # plt.plot(train_data.index, train_data['truk'], label='data training truk')
    # plt.plot(test_data.index, test_data['truk'], label='data asli truk')
    plt.plot(test_data.index, y_pred[:, 2], label='prediksi truk')
    plt.xlabel('Bulan')
    plt.ylabel('Penjualan')
    plt.title('penjualan kendaraan bermotor ')
    plt.legend()
    plt.show()