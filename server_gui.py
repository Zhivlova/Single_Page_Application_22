import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QLabel, QTableView, QDialog, QPushButton, \
    QLineEdit, QFileDialog, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import os


# GUI - Создание таблицы QModel, для отображения в окне программы.
def gui_create_model(database):
    list_items = database.items_list()
    list = QStandardItemModel()
    list.setHorizontalHeaderLabels(['Дата', 'Название', 'Количество', 'Расстояние'])
    for row in list_items:
        date, title, quantity, distance = row
        date = QStandardItem(date)
        date.setEditable(False)
        title = QStandardItem(title)
        title.setEditable(False)
        quantity = QStandardItem(str(quantity))
        quantity.setEditable(False)
        distance = QStandardItem(str(distance))
        distance.setEditable(False)
        list.appendRow([date, title, quantity, distance])
    return list


# Класс основного окна
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Кнопка выхода
        exitAction = QAction('Выход', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)

        # Кнопка обновить список
        self.refresh_button = QAction('Обновить список', self)

        # Статусбар
        # dock widget
        self.statusBar()

        # Тулбар
        self.toolbar = self.addToolBar('MainBar')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(self.refresh_button)

        # Настройки геометрии основного окна

        self.setFixedSize(800, 600)
        self.setWindowTitle('Sindle Page Application')

        self.label = QLabel('Список :', self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 25)

        self.items_list_table = QTableView(self)
        self.items_list_tablet.move(10, 45)
        self.items_list_table.setFixedSize(780, 400)


        self.show()

    app = QApplication(sys.argv)

    app.exec_()
