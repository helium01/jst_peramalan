import pandas as pd
import numpy as np
import itertools
import mysql.connector
import statsmodels.api as sm
from pylab import rcParams
import matplotlib.pyplot as plt



# Mendefinisikan fungsi untuk membuat model JST
# def create_model(input_shape):
#     model = tf.keras.Sequential([
#         tf.keras.layers.Dense(16, input_shape=input_shape, activation='relu'),
#         tf.keras.layers.Dense(1)
#     ])
#     model.compile(optimizer='adam', loss='mean_squared_error')
#     return model

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

# print(myresult)
# membuat dataframe dari hasil query
df = pd.DataFrame(myresult, columns=['id','jenis_kendaraan', 'tanggal', 'lokasi', 'jumlah_penjualan'])
# print(df.head())
# print(df.describe())
cols=['id','lokasi','jenis_kendaraan']
df.drop(cols,axis=1,inplace=True)
# print(df)

df.sort_values('tanggal')
df.isnull().sum()


df.tanggal = pd.to_datetime(df['tanggal'])
df['jumlah_penjualan'] = df['jumlah_penjualan'].astype(str).str.replace(',', '').astype(float)
df.groupby('tanggal')['jumlah_penjualan'].sum().reset_index()

df = df.set_index('tanggal')
df.index
y = df['jumlah_penjualan'].resample('MS').mean()
y['2022':]

print(y)
#
y.plot(figsize = (15, 6))
# plt.show()
rcParams['figure.figsize'] = 18, 8



# set the typical ranges for p, d, q
p = d = q = range(0, 2)

#take all possible combination for p, d and q
pdq = list(itertools.product(p, d, q))
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))



# Using Grid Search find the optimal set of parameters that yields the best performance
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(y, order = param, seasonal_order = param_seasonal, enforce_stationary = False,enforce_invertibility=False)
            result = mod.fit()
            print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, result.aic))
        except:
            continue

model = sm.tsa.statespace.SARIMAX(y, order = (1, 1, 1),
                                  seasonal_order = (1, 1, 0, 12)
                                 )
result = model.fit()
print(result.summary().tables[1])

prediction = result.get_prediction(start = pd.to_datetime('2021-01-01'), dynamic = False)
prediction_ci = prediction.conf_int()
prediction_ci
ax = y['2021':].plot(label = 'observed')
prediction.predicted_mean.plot(ax = ax, label = 'One-step ahead Forecast', alpha = 0.7, figsize = (14, 7))
ax.fill_between(prediction_ci.index, prediction_ci.iloc[:, 0], prediction_ci.iloc[:, 1], color = 'k', alpha = 0.2)
ax.set_xlabel("Date")
ax.set_ylabel('Sales')
# plt.legend()
# plt.show()



# Evaluation metrics are Squared Mean Error(SME) and Root Mean Squared Error(RMSE)
y_hat = prediction.predicted_mean
y_truth = y['2021-01-01':]

mse = ((y_hat - y_truth) ** 2).mean()
rmse = np.sqrt(mse)
print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
print('The Root Mean Squared Error of our forecasts is {}'.format(round(rmse, 2)))

pred_uc = result.get_forecast(steps = 100)
pred_ci = pred_uc.conf_int()
print(pred_uc)

def hasil():
    ax = y.plot(label = 'observed', figsize = (14, 7))
    pred_uc.predicted_mean.plot(ax = ax, label = 'forecast')
    ax.fill_between(pred_ci.index, pred_ci.iloc[:, 0], pred_ci.iloc[:, 1], color = 'k', alpha = 0.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Sales')

    plt.legend()
    plt.show()



