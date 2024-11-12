import sys
import numpy as np
from scipy.integrate import odeint
import pandas as pd
from sqlalchemy import create_engine
import matplotlib
import matplotlib.pyplot as plt

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QTableWidget, QTableWidgetItem


def templeButton(text, width, height):
    name = QPushButton(text)
    name.setFixedWidth(width)
    name.setFixedHeight(height)
    return name

def templeSlider(minRange, maxRange, SingleStep, PageStep, width, heigth):
    name = QSlider(Qt.Orientation.Horizontal, parent=None)
    name.setRange(minRange, maxRange)
    name.setSingleStep(SingleStep)
    name.setPageStep(PageStep)
    name.setTickPosition(QSlider.TickPosition.TicksAbove)
    name.setFixedWidth(width)
    name.setFixedHeight(heigth)
    return name

def updateDB(df):
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
            name='temperature',
            con=conn,
            if_exists='append',
            index=False
        )
def func_ode(y, t, k, b):
    dydt = k * y + b
    return dydt
# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() # Это прикалюха с взаимодействием Qt (Чтобы позволить Qt настраивать объект)

        self.setWindowTitle("My App")
        self.setStyleSheet("background-color: rgb(23,26,28);") #23,26,28

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
        widgetleft = QWidget()
        widgetleft.setStyleSheet(f"background-color: rgb(35,40,43);") #35,40,43
        layoutleft = QVBoxLayout()
        widgetleft.setLayout(layoutleft)

        # Настройка пространства для пространства графика
        widgetgragh = QWidget()
        widgetgragh.setStyleSheet(f"background-color: rgb(35,40,43);")
        self.layoutgraph = QVBoxLayout()
        widgetgragh.setLayout(self.layoutgraph)

        # Настройка пространства для пространства таблицы
        widgetTable = QWidget()
        widgetTable.setStyleSheet(f"background-color: rgb(255,255,255); color: black")
        self.layoutTable = QVBoxLayout()
        widgetTable.setLayout(self.layoutTable)

        #Определение таблицы
        self.table = QTableWidget()
        self.table.setColumnCount(2)# Устанавливаем количество столбцов
        self.table.setRowCount(101)
        self.table.setHorizontalHeaderLabels(['T_out', 'Time'])
        self.table.setStyleSheet(f"background-color:rgb(35,40,43), color: black")
        self.layoutTable.addWidget(self.table)

        # Определение Кнопок
        self.buttonGraf = templeButton("График", 120, 40)
        self.buttonGraf.clicked.connect(self.clickGraphClicked)
        self.Color(self.buttonGraf, "white")
        layoutleft.addWidget(self.buttonGraf)

        self.buttonResult = templeButton("Выход", 120, 40)
        self.Color(self.buttonResult, "white")
        self.buttonResult.clicked.connect(self.Exit)
        layoutleft.addWidget(self.buttonResult)

        # Определение Слайдеров
        sliderM = templeSlider(500, 1000, 10, 50, 150, 40)
        sliderM.valueChanged.connect(self.updateM)
        self.result_labelM = QLabel(f'Current Value M: {sliderM.value()}')
        self.result_labelM.setStyleSheet("QLabel{color: white;}")
        layoutleft.addWidget(self.result_labelM)
        layoutleft.addWidget(sliderM)

        sliderC1 = templeSlider(4200, 7200, 10, 300, 150, 40)
        sliderC1.valueChanged.connect(self.updateC1)
        self.result_labelC1 = QLabel(f'Current Value C1: {sliderC1.value()}')
        self.result_labelC1.setStyleSheet("QLabel{color: white;}")
        layoutleft.addWidget(self.result_labelC1)
        layoutleft.addWidget(sliderC1)

        sliderC2 = templeSlider(4200, 7200, 10, 300, 150, 40)
        sliderC2.valueChanged.connect(self.updateC2)
        self.result_labelC2 = QLabel(f'Current Value C2: {sliderC2.value()}')
        self.result_labelC2.setStyleSheet("QLabel{color: white;}")
        layoutleft.addWidget(self.result_labelC2)
        layoutleft.addWidget(sliderC2)

        sliderG1 = templeSlider(400, 1400, 10, 100, 150, 40)
        sliderG1.valueChanged.connect(self.updateG1)
        self.result_labelG1 = QLabel(f'Current Value G1: {sliderG1.value()}')
        self.result_labelG1.setStyleSheet("QLabel{color: white;}")
        layoutleft.addWidget(self.result_labelG1)
        layoutleft.addWidget(sliderG1)

        sliderG2 = templeSlider(1000, 2000, 10, 100, 150, 40)
        sliderG2.valueChanged.connect(self.updateG2)
        self.result_labelG2 = QLabel(f'Current Value G2: {sliderG1.value()}')
        self.result_labelG2.setStyleSheet("QLabel{color: white;}")
        layoutleft.addWidget(self.result_labelG2)
        layoutleft.addWidget(sliderG2)

        sliderT1 = templeSlider(90, 190, 10, 10, 150, 40)
        sliderT1.valueChanged.connect(self.updateT1)
        self.result_labelT1 = QLabel(f'Current Value T1: {sliderT1.value()}')
        self.result_labelT1.setStyleSheet("QLabel{color: white;}")
        layoutleft.addWidget(self.result_labelT1)
        layoutleft.addWidget(sliderT1)

        sliderT2 = templeSlider(20, 120, 10, 10, 150, 40)
        sliderT2.valueChanged.connect(self.updateT2)
        self.result_labelT2 = QLabel(f'Current Valuea T2: {sliderT2.value()}')
        self.result_labelT2.setStyleSheet("QLabel{color: white;}")
        layoutleft.addWidget(self.result_labelT2)
        layoutleft.addWidget(sliderT2)

        sliderTmax = templeSlider(10, 50, 10, 5, 150, 40)
        sliderTmax.valueChanged.connect(self.updateTmax)
        self.result_labelTmax = QLabel(f'Current Value Tmax: {sliderTmax.value()}')
        self.result_labelTmax.setStyleSheet("QLabel{color: white;}")
        layoutleft.addWidget(self.result_labelTmax)
        layoutleft.addWidget(sliderTmax)

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
        layoutmain.addSpacing(50)
        layoutmain.addWidget(widgetTable)
        layoutmain.addSpacing(30)

        widget = QWidget()
        widget.setLayout(layoutmain)
        self.setCentralWidget(widget)
    # Функции, которые отвечает, за то, что будет происходить при нажатии на соответствующие кнопки, и изменении графиков
    def Exit(self):
        exit()
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
        df = pd.DataFrame(self.T_out[:,0,0,0,0].reshape((1, self.ntime)))
        df.insert(0, 'T2', self.T2)
        df.insert(0, 'T1', self.T1)
        df.insert(0, 'G2', self.G2)
        df.insert(0, 'G1', self.G1)
        df.insert(0, 'C2', self.C2)
        df.insert(0, 'C1', self.C1)
        df.insert(0, 'M', self.M)
        df.insert(0, 'tmax', self.tmax)

        # Внесение данных в таблицу
        i = 0
        while i < t.size:
            itemT = QTableWidgetItem(str(t[i]))
            itemSol = QTableWidgetItem(str(sol[i]))
            self.table.setItem(i, 0, itemT)
            self.table.setItem(i,1,itemSol)
            i = i+1

        # Обновление графика
        fig, ax = plt.subplots()
        ax.plot(t, sol, color='green', label='График функции')
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

    def updateM(self, value):
        self.result_labelM.setText(f'Current Value M: {value}')
        self.M = value

    def updateC1(self, value):
        self.result_labelC1.setText(f'Current Value C1: {value}')
        self.C1 = value

    def updateC2(self, value):
        self.result_labelC2.setText(f'Current Value C2: {value}')
        self.C2 = value

    def updateG1(self, value):
        self.result_labelG1.setText(f'Current Value G1: {value}')
        self.G1 = value

    def updateG2(self, value):
        self.result_labelG2.setText(f'Current Value G2: {value}')
        self.G2 = value

    def updateT1(self, value):
        self.result_labelT1.setText(f'Current Value T1: {value}')
        self.T1 = value

    def updateT2(self, value):
        self.result_labelT2.setText(f'Current Value T2: {value}')
        self.T2 = value

    def updateTmax(self, value):
        self.result_labelTmax.setText(f'Current Value Tmax: {value}')
        self.Tmax = value

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()