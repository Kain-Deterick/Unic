import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor, QPixmap, QIntValidator
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QTableWidget, QTableWidgetItem, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__() # Это прикалюха с взаимодействием Qt (Чтобы позволить Qt настраивать объект)

        self.setWindowTitle("My App")
        self.setStyleSheet("background-color: rgb(23,26,28);") #23,26,28

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()