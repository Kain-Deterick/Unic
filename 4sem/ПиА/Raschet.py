import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
from sqlalchemy import create_engine

length = 350 # Размер генерируемых данных

# Объявление переменных
flow_water = [float(f'{np.random.uniform(5250, 9000):.3f}') for i in range(length)]
flow_dust = [float(f'{np.random.uniform(16500, 23000):.3f}') for i in range(length)]
temp_air = [float(f'{np.random.uniform(5000, 10000):.3f}') for i in range(length)]
temp_nikel = [float(f'{np.random.uniform(20000, 24000):.3f}') for i in range(length)]
current_time = datetime.datetime.now()
timestamps = []

# Передаточные функции для первого выходного параметра
W1 = lambda p: 425 / (0.0000003 * p ** 2 + 0.0000007 * p + 1)
W2 = lambda p: 450 / (0.0000005 * p ** 2 + 0.0000005 * p + 1)
W3 = lambda p: 500 / (0.0000001 * p ** 2 + 0.0000009 * p + 1)
W4 = lambda p: 525 / (0.0000004 * p ** 2 + 0.0000006 * p + 1)


temperature = [float( f'{(W1(flow_water[i] - 6150) - W2(flow_dust[i] - 7200) + W3(temp_air[i] - 21000) + W4(temp_nikel[i] - 17000)):.3f}') for i in range(350)]


current_time = datetime.datetime.now()


for i in range(length):
    timestamps.append(current_time.replace(microsecond=0)) # добавляем текeщее время в список меток времени
    current_time += datetime.timedelta(minutes=5) # увеличиваем текущее время на заданный интервал

#Вывод на график
#x_data = range(length)

#plt.title('Температура в печи кипящего слоя')
#plt.xlabel('Номер измерения')
#plt.ylabel('Температура')
#plt.legend()
#plt.show()


df = pd.DataFrame({'Текущее время': timestamps,
                      'Расход воды': flow_water,
                      'Расход никеля': temp_nikel,
                      'Расход оборотной пыли': flow_dust,
                      'Расход воздушного дутья': temp_air,
                      'Температура в печи кипящего слоя': temperature})

#df.to_excel("outfile.xlsx", engine='xlsxwriter') - это для проверки
#Сортировка значений перед занесением в базу данных
df = df.loc[df['Температура в печи кипящего слоя'] >= 250]
df = df.loc[df['Температура в печи кипящего слоя'] <= 500]

#докачать SQLAlchemy
#Подключение к базе данных

# The database URL must be in a specific format
db_url = "mysql+mysqlconnector://{USER}:{PWD}@{HOST}/{DBNAME}"
# Replace the values below with your own
# DB username, password, host and database name
db_url = db_url.format(
    USER = "Kain",
    PWD = "Uxninitcroom13",
    HOST = "localhost:3306",
    DBNAME = "PIA"
)
# Create the DB engine instance. We'll use
# this engine to connect to the database

engine = create_engine(db_url,echo=False)

with engine.begin() as conn:
    df.to_sql(
        name='temperature',
        con = conn,
        index=False
    )