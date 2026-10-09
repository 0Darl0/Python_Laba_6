import sqlite3

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QTableWidgetItem, QComboBox

booling = {0: False, 1: True}


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 507)
        Form.setStyleSheet("background-color: rgb(49, 49, 49);")
        self.atchive_table = QtWidgets.QTableWidget(Form)
        self.atchive_table.setGeometry(QtCore.QRect(10, 50, 381, 441))
        self.atchive_table.setObjectName("atchive_table")
        self.atchive_table.setColumnCount(0)
        self.atchive_table.setRowCount(0)
        self.back_button = QtWidgets.QPushButton(Form)
        self.back_button.setGeometry(QtCore.QRect(10, 10, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        self.back_button.setFont(font)
        self.back_button.setStyleSheet("color: white;")
        self.back_button.setObjectName("back_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Archive"))
        self.back_button.setText(_translate("Form", "Назад"))


class Archive(Ui_Form, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.back_button.clicked.connect(self.close)
        self.ownerid = ''
        self.con = sqlite3.connect('account.db')

    def table(self):
        cur = self.con.cursor()
        result = cur.execute(
            "SELECT Name, priority, Time,"
            " Ready, isDelete FROM target WHERE ownerID=? AND (Ready = ? OR isDelete = ?)",
            (self.ownerid, 1, 1,)).fetchall()
        if result:
            self.atchive_table.setRowCount(len(result))
            self.atchive_table.setColumnCount(len(result[0]))
            # Заполнили таблицу полученными элементами
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    if j == 1:
                        qcombo = QComboBox()
                        qcombo.addItems(['Менее важно', 'Важно', 'Очень важно', 'Абсолютно важно!!!'])
                        qcombo.setCurrentIndex(int(val) - 1)
                        qcombo.setEnabled(False)
                        self.atchive_table.setCellWidget(i, j, qcombo)
                    elif j == 2:
                        if val:
                            item = QTableWidgetItem(val)
                        else:
                            item = QTableWidgetItem("Не указано")
                        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                        self.atchive_table.setItem(i, j, item)
                    elif j > 2:
                        qcheck = QCheckBox()
                        qcheck.setChecked(booling[val])
                        qcheck.setEnabled(False)
                        self.atchive_table.setCellWidget(i, j, qcheck)
            self.atchive_table.setHorizontalHeaderLabels(['Название', 'Приоритет', 'Время', 'Выполнено', 'Удалить'])

    def Tema(self, isWhite):
        if not isWhite:
            self.setStyleSheet('background-color: rgb(49, 49, 49)')
            self.back_button.setStyleSheet('color: white')
        else:
            self.setStyleSheet('background-color: rgb(255, 255, 255)')
            self.back_button.setStyleSheet('color: black')
