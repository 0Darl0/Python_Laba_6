import datetime as dt
import sqlite3

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QMessageBox


class Ui_CreateObject(object):
    def setupUi(self, CreateObject):
        CreateObject.setObjectName("CreateObject")
        CreateObject.resize(390, 329)
        CreateObject.setStyleSheet("background-color: rgb(230, 255, 190);")
        self.exitButton = QtWidgets.QPushButton(CreateObject)
        self.exitButton.setGeometry(QtCore.QRect(10, 20, 91, 31))
        self.exitButton.setObjectName("exitButton")
        self.CreateButton = QtWidgets.QPushButton(CreateObject)
        self.CreateButton.setGeometry(QtCore.QRect(290, 20, 91, 31))
        self.CreateButton.setObjectName("CreateButton")
        self.name_create = QtWidgets.QTextEdit(CreateObject)
        self.name_create.setGeometry(QtCore.QRect(10, 110, 371, 41))
        self.name_create.setObjectName("name_create")
        self.nametext = QtWidgets.QLabel(CreateObject)
        self.nametext.setGeometry(QtCore.QRect(10, 80, 121, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.nametext.setFont(font)
        self.nametext.setObjectName("nametext")
        self.prioritycombo = QtWidgets.QComboBox(CreateObject)
        self.prioritycombo.setGeometry(QtCore.QRect(10, 200, 131, 21))
        self.prioritycombo.setObjectName("prioritycombo")
        self.prioritycombo.addItem("")
        self.prioritycombo.addItem("")
        self.prioritycombo.addItem("")
        self.prioritycombo.addItem("")
        self.prioritytext = QtWidgets.QLabel(CreateObject)
        self.prioritytext.setGeometry(QtCore.QRect(10, 170, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.prioritytext.setFont(font)
        self.prioritytext.setObjectName("prioritytext")
        self.Datetext = QtWidgets.QLabel(CreateObject)
        self.Datetext.setGeometry(QtCore.QRect(10, 240, 371, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.Datetext.setFont(font)
        self.Datetext.setObjectName("Datetext")
        self.Dateinput = QtWidgets.QTextEdit(CreateObject)
        self.Dateinput.setGeometry(QtCore.QRect(10, 270, 371, 41))
        self.Dateinput.setObjectName("Dateinput")
        self.CreateLabelText = QtWidgets.QLabel(CreateObject)
        self.CreateLabelText.setGeometry(QtCore.QRect(135, 30, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.CreateLabelText.setFont(font)
        self.CreateLabelText.setObjectName("CreateLabelText")

        self.retranslateUi(CreateObject)
        QtCore.QMetaObject.connectSlotsByName(CreateObject)

    def retranslateUi(self, CreateObject):
        _translate = QtCore.QCoreApplication.translate
        CreateObject.setWindowTitle(_translate("CreateObject", "Создание цели"))
        self.exitButton.setText(_translate("CreateObject", "Отменить"))
        self.CreateButton.setText(_translate("CreateObject", "Создать"))
        self.name_create.setPlaceholderText(_translate("CreateObject", "Зарядка, Медитация и т.д."))
        self.nametext.setText(_translate("CreateObject", "Название"))
        self.prioritycombo.setItemText(0, _translate("CreateObject", "Менее важно"))
        self.prioritycombo.setItemText(1, _translate("CreateObject", "Важно"))
        self.prioritycombo.setItemText(2, _translate("CreateObject", "Очень важно"))
        self.prioritycombo.setItemText(3, _translate("CreateObject", "Абсолютно важно!!!"))
        self.prioritytext.setText(_translate("CreateObject", "Приоритет"))
        self.Datetext.setText(_translate("CreateObject", "Время выполнения (ДД.ММ.ГГГГ)"))
        self.Dateinput.setPlaceholderText(_translate("CreateObject", "Например: 31.12.2024"))
        self.CreateLabelText.setText(_translate("CreateObject", "Создание цели"))


class CreateTarget(Ui_CreateObject, QMainWindow):
    def __init__(self, Main_Menu):
        super().__init__()
        self.main_menu = Main_Menu
        self.ownerID = ''
        self.con = sqlite3.connect('account.db')
        self.setupUi(self)
        self.exitButton.clicked.connect(self.close)
        self.CreateButton.clicked.connect(self.createtarget)

    def createtarget(self):
        if self.name_create.toPlainText().strip() == '':
            QMessageBox.critical(self, "Ошибка ", "Вы не указали название цели", QMessageBox.Ok)
            return

        date_text = self.Dateinput.toPlainText().strip()

        if date_text:
            try:
                parts = date_text.split('.')
                if len(parts) != 3:
                    raise ValueError("Неверный формат")

                day = int(parts[0])
                month = int(parts[1])
                year = int(parts[2])
                if month < 1 or month > 12:
                    raise ValueError("Месяц должен быть от 1 до 12")
                if day < 1 or day > 31:
                    raise ValueError("День должен быть от 1 до 31")
                if year < 2000 or year > 2100:
                    raise ValueError("Год должен быть от 2000 до 2100")
                test_date = dt.date(year, month, day)
                formatted_date = f"{day:02d}.{month:02d}.{year}"

            except Exception as e:
                QMessageBox.critical(self, "Ошибка",
                                     f"Неправильная дата: {e}\n\nИспользуйте формат: ДД.ММ.ГГГГ\nПример: 31.12.2024",
                                     QMessageBox.Ok)
                return
        else:
            formatted_date = ''

        cur = self.con.cursor()
        title_priority = self.prioritycombo.currentText()
        priority_id = cur.execute("SELECT id FROM priority WHERE title = ?", (title_priority,)).fetchone()[0]

        cur.execute("SELECT MAX(idtarget) FROM target")
        max_id = cur.fetchone()[0]
        new_id = (max_id or 0) + 1

        cur.execute('INSERT INTO target VALUES (?, ?, ?, ?, ?, ?, ?)',
                    (new_id, self.ownerID, self.name_create.toPlainText(),
                     priority_id, formatted_date, 0, 0))
        self.con.commit()
        self.main_menu.Update()
        self.close()

    def Tema(self, isWhite):
        if not isWhite:
            self.setStyleSheet('background-color: rgb(49, 49, 49)')
            self.exitButton.setStyleSheet('color: white')
            self.CreateButton.setStyleSheet('color: white')
            self.name_create.setStyleSheet('color: white')
            self.nametext.setStyleSheet('color: white')
            self.CreateLabelText.setStyleSheet('color: white')
            self.prioritytext.setStyleSheet('color: white')
            self.prioritycombo.setStyleSheet('color: white')
            self.Dateinput.setStyleSheet('color: white')
            self.Datetext.setStyleSheet('color: white')
        else:
            self.setStyleSheet('background-color: rgb(255, 255, 255)')
            self.exitButton.setStyleSheet('color: black')
            self.CreateButton.setStyleSheet('color: black')
            self.name_create.setStyleSheet('color: black')
            self.nametext.setStyleSheet('color: black')
            self.CreateLabelText.setStyleSheet('color: black')
            self.prioritytext.setStyleSheet('color: black')
            self.prioritycombo.setStyleSheet('color: black')
            self.Dateinput.setStyleSheet('color: black')
            self.Datetext.setStyleSheet('color: black')