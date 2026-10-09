import sqlite3
import webbrowser

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from Hash import hashpassword
from checkpassword import password_level


class Login_Ui(object):
    def setupUi(self, Login_2):
        Login_2.setObjectName("Login_2")
        Login_2.resize(361, 232)
        Login_2.setStyleSheet("background-color: rgb(230, 255, 190);")
        self.regButton = QtWidgets.QPushButton(Login_2)
        self.regButton.setGeometry(QtCore.QRect(190, 194, 161, 23))
        self.regButton.setObjectName("regButton")
        self.error_text = QtWidgets.QLabel(Login_2)
        self.error_text.setGeometry(QtCore.QRect(10, 170, 341, 16))
        self.error_text.setText("")
        self.error_text.setObjectName("label")
        self.loginButton = QtWidgets.QPushButton(Login_2)
        self.loginButton.setGeometry(QtCore.QRect(10, 194, 161, 23))
        self.loginButton.setObjectName("loginButton")
        self.Password_text = QtWidgets.QLineEdit(Login_2)
        self.Password_text.setGeometry(QtCore.QRect(10, 87, 341, 71))
        self.Password_text.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Password_text.setObjectName("Password_text")
        self.Login_text = QtWidgets.QLineEdit(Login_2)
        self.Login_text.setGeometry(QtCore.QRect(10, 10, 341, 71))
        self.Login_text.setObjectName("Login_text")

        self.retranslateUi(Login_2)
        QtCore.QMetaObject.connectSlotsByName(Login_2)

    def retranslateUi(self, Login_2):
        _translate = QtCore.QCoreApplication.translate
        Login_2.setWindowTitle(_translate("Login_2", "Вход"))
        self.regButton.setText(_translate("Login_2", "Зарегистрироваться"))
        self.Login_text.setPlaceholderText(_translate("Login_2", "Логин..."))
        self.Password_text.setPlaceholderText(_translate("Login_2", "Пароль..."))
        self.loginButton.setText(_translate("Login_2", "Войти"))


class Logins_Register(Login_Ui, QMainWindow):
    closelog = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('account.db')
        self.setupUi(self)
        self.loginButton.clicked.connect(self.login)
        self.regButton.clicked.connect(self.register)
        self.logins = ''
        self.idowner = ''

    def login(self):
        cur = self.con.cursor()
        logins = cur.execute('''SELECT login FROM login_password''').fetchall()
        for login in logins:
            if login[0] == self.Login_text.text():
                if cur.execute('''SELECT password FROM login_password WHERE login = ?''',
                               (self.Login_text.text(),)).fetchall()[0][0] == hashpassword(
                    self.Password_text.text()):
                    if self.Login_text.text() == 'Andrey':
                        webbrowser.open('https://www.youtube.com/watch?v=dQw4w9WgXcQ', new=2)
                    self.logins = login[0]
                    self.idowner = \
                        cur.execute('''SELECT id FROM login_password WHERE login = ?''', (login[0],)).fetchall()[0][0]
                    self.close()
        self.error_text.setText('Неверный логин или пароль, попробуйте заново')

    def register(self):
        cur = self.con.cursor()
        logins = cur.execute('''SELECT login FROM login_password''').fetchall()
        error = False
        for login in logins:
            if login[0] == self.Login_text.text():
                self.error_text.setText('Аккаунт с таким логином существует')
                error = True
        if self.Login_text.text() == '':
            self.error_text.setText('Логин аккаунта не может быть пустым')
            error = True
        if not error:
            if password_level(self.Password_text.text()) != '1':
                self.error_text.setText(password_level(self.Password_text.text()))
            else:
                cur.execute('INSERT INTO login_password VALUES (?, ?, ?)',
                            (len(logins) + 1, self.Login_text.text(),
                             hashpassword(self.Password_text.text())))
                self.logins = self.Login_text.text()
                self.idowner = len(logins) + 1
                self.con.commit()
                self.close()

    def Tema(self, isWhite):
        if not isWhite:
            self.setStyleSheet('background-color: rgb(49, 49, 49)')
            self.loginButton.setStyleSheet('color: white')
            self.regButton.setStyleSheet('color: white')
            self.Login_text.setStyleSheet('color: white')
            self.Password_text.setStyleSheet('color: white')
        else:
            self.setStyleSheet('background-color: rgb(255, 255, 255)')
            self.loginButton.setStyleSheet('color: black')
            self.regButton.setStyleSheet('color: black')
            self.Login_text.setStyleSheet('color: black')
            self.Password_text.setStyleSheet('color: black')

    def closeEvent(self, event):
        self.closelog.emit()
