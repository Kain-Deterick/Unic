import sys
import numpy as np
from scipy.integrate import odeint
import pandas as pd
from sqlalchemy import create_engine
import matplotlib
import matplotlib.pyplot as plt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QPixmap, QIntValidator
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QTableWidget, QTableWidgetItem, QLineEdit


def templeButton(text, width, height):  # Функция 1
    name = QPushButton(text)
    name.setFixedWidth(width)
    name.setFixedHeight(height)
    return name

def updateDB(df):  # Функция  2
    # The database URL must be in a specific format
    db_url = "mysql+mysqlconnector://{USER}:{PWD}@{HOST}/{DBNAME}"
    # Replace the values below with your own
    # DB username, password, host and database name
    db_url = db_url.format(
        USER="Kain",
        PWD="Uxninitcroom13",
        HOST="localhost:3306",
        DBNAME="unic"
    )
    engine = create_engine(db_url, echo=False)

    with engine.begin() as conn:
        df.to_sql(
            name='temperature1',
            con=conn,
            if_exists='append',
            index=False
        )
def func_ode(y, t, k, b): # Функция 3 (Описание диффуры)
    dydt = k * y + b
    return dydt
# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow): # Создание класса окна (Используя готовый шаблон)
    def __init__(self):
        super().__init__() # Это прикалюха с взаимодействием Qt (Чтобы позволить Qt настраивать объект)

        self.setWindowTitle("My App") # Задаем название
        self.setStyleSheet("background-color: rgb(23,26,28);") #23,26,28 меняем фон

        #Переменные
        self.tmax = 10
        self.M = 500
        self.C1 = 4200
        self.C2 = 4200
        self.G1 = 400
        self.G2 = 1000
        self.T1 = 90
        self.T2 = 20
        self.k = 0
        self.t = 0
        self.T_out_0 = 0  # initial value
        self.ntime = 101  # number of time nodes
        self.T_out = np.ndarray((self.ntime, 1, 1, 1, 1))  # result array


        layoutmain = QHBoxLayout()
        # Настройка пространства для левого пространства
        widgetleft = QWidget() # Создаем пустой виджет (Для изменения заднего фона)
        widgetleft.setStyleSheet(f"background-color: rgb(35,40,43);") #35,40,43
        layoutleft = QVBoxLayout()
        widgetleft.setLayout(layoutleft)

        # Настройка пространства для пространства графика
        widgetgragh = QWidget()
        widgetgragh.setStyleSheet(f"background-color: rgb(255,182,193);")
        self.layoutgraph = QVBoxLayout()
        widgetgragh.setLayout(self.layoutgraph)

        # Определение Кнопок
        self.buttonGraf = templeButton("График", 120, 40) # Используется функция 1
        self.buttonGraf.clicked.connect(self.clickGraphClicked)
        self.Color(self.buttonGraf, "lightPink")
        layoutleft.addWidget(self.buttonGraf)

        # Задание коэффициентов
        self.LineEdit_M = QLineEdit("500")
        self.LineEdit_M.setStyleSheet("background-color: rgb(255,255,255)")
        # Создание строки текста перед строкой ввода
        self.result_labelM = QLabel(f'Введите значение в диапазоне [500:1000].Текущее значение M: {int(self.LineEdit_M.text())}')
        self.result_labelM.setStyleSheet("QLabel{color: white;}")
        self.LineEdit_M.setValidator(QIntValidator(500, 1000))
        self.LineEdit_M.editingFinished.connect(self.updateM)
        layoutleft.addWidget(self.result_labelM)
        layoutleft.addWidget(self.LineEdit_M)

        self.LineEdit_C1 = QLineEdit("4200")
        self.LineEdit_C1.setStyleSheet("background-color: rgb(255,255,255)")
        self.result_labelC1 = QLabel(f'Введите значение в диапазоне [4200:7200].Текущее значение C1: {int(self.LineEdit_C1.text())}')
        self.result_labelC1.setStyleSheet("QLabel{color: white;}")
        self.LineEdit_C1.setValidator(QIntValidator(4200, 7200))
        self.LineEdit_C1.editingFinished.connect(self.updateC1)
        layoutleft.addWidget(self.result_labelC1)
        layoutleft.addWidget(self.LineEdit_C1)

        self.LineEdit_C2 = QLineEdit("4200")
        self.LineEdit_C2.setStyleSheet("background-color: rgb(255,255,255)")
        self.result_labelC2 = QLabel(f'Введите значение в диапазоне [4200:7200].Текущее значение C2: {int(self.LineEdit_C2.text())}')
        self.result_labelC2.setStyleSheet("QLabel{color: white;}")
        self.LineEdit_C2.setValidator(QIntValidator(4200, 7200))
        self.LineEdit_C2.editingFinished.connect(self.updateC2)
        layoutleft.addWidget(self.result_labelC2)
        layoutleft.addWidget(self.LineEdit_C2)

        self.LineEdit_G1 = QLineEdit("400")
        self.LineEdit_G1.setStyleSheet("background-color: rgb(255,255,255)")
        self.result_labelG1 = QLabel(f'Введите значение в диапазоне [400:1400].Текущее значение G1: {int(self.LineEdit_G1.text())}')
        self.result_labelG1.setStyleSheet("QLabel{color: white;}")
        self.LineEdit_G1.setValidator(QIntValidator(400, 1400))
        self.LineEdit_G1.editingFinished.connect(self.updateG1)
        layoutleft.addWidget(self.result_labelG1)
        layoutleft.addWidget(self.LineEdit_G1)

        self.LineEdit_G2 = QLineEdit("1000")
        self.LineEdit_G2.setStyleSheet("background-color: rgb(255,255,255)")
        self.result_labelG2 = QLabel(f'Введите значение в диапазоне [1000:2000].Текущее значение G2: {int(self.LineEdit_G2.text())}')
        self.result_labelG2.setStyleSheet("QLabel{color: white;}")
        self.LineEdit_G2.setValidator(QIntValidator(1000, 2000))
        self.LineEdit_G2.editingFinished.connect(self.updateG2)
        layoutleft.addWidget(self.result_labelG2)
        layoutleft.addWidget(self.LineEdit_G2)

        self.LineEdit_T1 = QLineEdit("90")
        self.LineEdit_T1.setStyleSheet("background-color: rgb(255,255,255)")
        self.result_labelT1 = QLabel(f'Введите значение в диапазоне [90:190].Текущее значение T1: {int(self.LineEdit_T1.text())}')
        self.result_labelT1.setStyleSheet("QLabel{color: white;}")
        self.LineEdit_T1.setValidator(QIntValidator(90, 190))
        self.LineEdit_T1.editingFinished.connect(self.updateT1)
        layoutleft.addWidget(self.result_labelT1)
        layoutleft.addWidget(self.LineEdit_T1)

        self.LineEdit_T2 = QLineEdit("20")
        self.LineEdit_T2.setStyleSheet("background-color: rgb(255,255,255)")
        self.result_labelT2 = QLabel(f'Введите значение в диапазоне [20:120].Текущее значение T2: {int(self.LineEdit_T2.text())}')
        self.result_labelT2.setStyleSheet("QLabel{color: white;}")
        self.LineEdit_T2.setValidator(QIntValidator(20, 120))
        self.LineEdit_T2.editingFinished.connect(self.updateT2)
        layoutleft.addWidget(self.result_labelT2)
        layoutleft.addWidget(self.LineEdit_T2)

        self.LineEdit_Tmax = QLineEdit("10")
        self.LineEdit_Tmax.setStyleSheet("background-color: rgb(255,255,255)")
        self.result_labelTmax = QLabel(f'Введите значение в диапазоне [10:50].Текущее значение Tmax: {int(self.LineEdit_Tmax.text())}')
        self.result_labelTmax.setStyleSheet("QLabel{color: white;}")
        self.LineEdit_Tmax.setValidator(QIntValidator(10, 50))
        self.LineEdit_Tmax.editingFinished.connect(self.updateTmax)
        layoutleft.addWidget(self.result_labelTmax)
        layoutleft.addWidget(self.LineEdit_Tmax)

# Начальный пустой график
        fig, ax = plt.subplots()
        ax.set_title('M=' + str(self.M) + ', C1=' + str(self.C1) + ', C2=' + str(self.C1) + ', G1=' + str(self.G1) +
                     ', G2=' + str(self.G2) + ', T1=' + str(self.T1) + ', T2=' + str(self.T2))
        fig.savefig('foo')
        plt.close(fig)
        self.labelgragh = QLabel(self)
        pixmap = QPixmap('foo.png')
        self.labelgragh.setPixmap(pixmap)

        #Позиционирование приложения
        self.layoutgraph.addWidget(self.labelgragh)
        layoutmain.addSpacing(30)
        layoutmain.addWidget(widgetleft)
        layoutmain.addSpacing(50)
        layoutmain.addWidget(widgetgragh)
        layoutmain.addSpacing(30)

        widget = QWidget()
        widget.setLayout(layoutmain)
        self.setCentralWidget(widget)

    # Функции, которые отвечает, за то, что будет происходить при нажатии на соответствующие кнопки, и изменении графиков
    def Color(self, name, color):
        name.setAutoFillBackground(True)

        palette = name.palette()
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(color))
        name.setPalette(palette)

    def clickGraphClicked(self):
        # Решение диффуры
        global t
        t = np.linspace(0, self.tmax, self.ntime)
        if self.G1 == 0 and self.G2 == 0:
            self.k = -0.5*(self.C1 + self.C2)/self.M
            self.b = -0.5*(self.T1*(self.C1+1.0) + self.T2 * (self.C2+1.0))/self.M
        else:
            self.k = -(self.C1*self.G1 + self.C2*self.G2)/(self.M*(self.G1+self.G2))
            self.b = (self.T1*self.G1*(self.C1+1.0) + self.T2*self.G2*(self.C2+1.0))/(self.M*(self.G1+self.G2))
        sol = odeint(func_ode, self.T_out_0, t, args=(self.k, self.b)).reshape(self.ntime, )

        self.T_out[:,0,0,0,0] = sol
        # Занесение данных в диффуру
        df = pd.DataFrame(self.T_out[:,0,0,0,0].reshape((1, self.ntime)))
        df.insert(0, 'T2', self.T2)
        df.insert(0, 'T1', self.T1)
        df.insert(0, 'G2', self.G2)
        df.insert(0, 'G1', self.G1)
        df.insert(0, 'C2', self.C2)
        df.insert(0, 'C1', self.C1)
        df.insert(0, 'M', self.M)
        df.insert(0, 'tmax', self.tmax)

        # Обновление графика
        fig, ax = plt.subplots()
        ax.plot(t, sol, color='pink', label='График функции')
        ax.set_xlabel('Time')
        ax.set_ylabel('Temperature')
        ax.set_title('M=' + str(self.M) + ', C1=' + str(self.C1) + ', C2=' + str(self.C1) + ', G1=' + str(self.G1) +
                   ', G2=' + str(self.G2) + ', T1=' + str(self.T1) + ', T2=' + str(self.T2))
        ax.legend()
        fig.savefig('foo')
        plt.close(fig)
        pixmap = QPixmap('foo.png')
        self.labelgragh.setPixmap(pixmap)
        # Занесение в базу данных
        updateDB(df)

    #Функцмм реакции приложения ввода значений пользователем
    def updateM(self):
        #Изменения строки значения переменных
        self.result_labelM.setText(f'Введите значение в диапазоне [500:1000].Текущее значение M: {int(self.LineEdit_M.text())}')
        # Обновления соответствующей переменной для расчетов 
        self.M = int(self.LineEdit_M.text())

    def updateC1(self):
        self.result_labelC1.setText(f'Введите значение в диапазоне [4200:7200].Текущее значение C1: {int(self.LineEdit_C1.text())}')
        self.C1 = int(self.LineEdit_C1.text())

    def updateC2(self):
        self.result_labelC2.setText(f'Введите значение в диапазоне [4200:7200].Текущее значение C2: {int(self.LineEdit_C2.text())}')
        self.C2 = int(self.LineEdit_C2.text())

    def updateG1(self):
        self.result_labelG1.setText(f'Введите значение в диапазоне [400:1400].Текущее значение G1: {int(self.LineEdit_G1.text())}')
        self.G1 = int(self.LineEdit_G1.text())

    def updateG2(self):
        self.result_labelG2.setText(f'Введите значение в диапазоне [1000:2000].Текущее значение G2: {int(self.LineEdit_G2.text())}')
        self.G2 = int(self.LineEdit_G2.text())
    def updateT1(self):
        self.result_labelT1.setText(f'Введите значение в диапазоне [90:190].Текущее значение T1: {int(self.LineEdit_T1.text())}')
        self.T1 = int(self.LineEdit_T1.text())

    def updateT2(self):
        self.result_labelT2.setText(f'Введите значение в диапазоне [20:120].Текущее значение T2: {int(self.LineEdit_T2.text())}')
        self.T2 = int(self.LineEdit_T2.text())

    def updateTmax(self):
        self.result_labelTmax.setText(f'Введите значение в диапазоне [10:50].Текущее значение Tmax: {int(self.LineEdit_Tmax.text())}')
        self.Tmax = int(self.LineEdit_Tmax.text())

app = QApplication(sys.argv) # Создание процесса приложения (QApplication - модуль создания процесса)

window = MainWindow() # Передача процессу окна
window.show() # Отображение окна

app.exec() # Включение цикла обработки событий