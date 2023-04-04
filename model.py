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
# print(df.set_index('bulan'))

# normalisasi data
scaler = MinMaxScaler()
df_norm = scaler.fit_transform(df)

# mempersiapkan data latih dan data uji
X_train, y_train = df_norm[:-12, :-2], df_norm[:-12, -2:]
X_test, y_test = df_norm[-12:, :-2], df_norm[-12:, -2:]

# membuat model jaringan saraf tiruan
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(units=32, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(units=2)
])
# menentukan optimizer dan loss function untuk model
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01), loss='mse')

# melatih model pada data latih
history = model.fit(X_train, y_train, epochs=100, batch_size=8, verbose=0, validation_split=0.1)


# menampilkan grafik loss function pada data latih dan data validasi
def grafik():
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Training and Validation Loss')
    plt.legend()
    plt.show()

# menyimpan model yang telah dilatih
model.save('model.h5')