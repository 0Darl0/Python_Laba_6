import csv
import sqlite3
import sys

from PyQt5 import QtCore, QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QCheckBox, QComboBox, QMessageBox

from archive import Archive
from creatyeobject import CreateTarget
from logpass import Logins_Register
from tg_bot import check_binding_status
from tg_form import TelegramBindingWindow

booling = {0: False, 1: True}
Combo = {'Менее важно': 1, 'Важно': 2, 'Очень важно': 3, 'Абсолютно важно!!!': 4}


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(436, 600)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addtarget_Button = QtWidgets.QPushButton(self.centralwidget)
        self.addtarget_Button.setGeometry(QtCore.QRect(370, 10, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.addtarget_Button.setFont(font)
        self.addtarget_Button.setObjectName("addtarget_Button")
        self.targetTable = QtWidgets.QTableWidget(self.centralwidget)
        self.targetTable.setGeometry(QtCore.QRect(20, 60, 391, 471))
        self.targetTable.setObjectName("targetTable")
        self.hello_label = QtWidgets.QLabel(self.centralwidget)
        self.hello_label.setGeometry(QtCore.QRect(20, 5, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.hello_label.setFont(font)
        self.hello_label.setText("")
        self.hello_label.setObjectName("hello_label")
        self.Archive_button = QtWidgets.QPushButton(self.centralwidget)
        self.Archive_button.setGeometry(QtCore.QRect(290, 520, 121, 31))
        self.Archive_button.setObjectName("Archive_button")
        self.Tema_button = QtWidgets.QPushButton(self.centralwidget)
        self.Tema_button.setGeometry(QtCore.QRect(20, 520, 31, 31))
        self.Tema_button.setObjectName("Tema_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.Telegram_button = QtWidgets.QPushButton(self.centralwidget)
        self.Telegram_button.setGeometry(QtCore.QRect(60, 520, 100, 31))
        self.Telegram_button.setObjectName("Telegram_button")
        self.Telegram_button.setText("📱 Привязать TG")
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 436, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuAccount = QtWidgets.QMenu(self.menubar)
        self.menuAccount.setObjectName("menuAccount")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.Createtarget_action = QtWidgets.QAction(MainWindow)
        self.Createtarget_action.setObjectName("Createtarget_action")
        self.actionLogin = QtWidgets.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.actionLog_Out = QtWidgets.QAction(MainWindow)
        self.actionLog_Out.setObjectName("actionLog_Out")
        self.Save_CSV_action = QtWidgets.QAction(MainWindow)
        self.Save_CSV_action.setObjectName("Save_CSV_action")
        self.menuEdit.addAction(self.Createtarget_action)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.Save_CSV_action)
        self.menuAccount.addAction(self.actionLogin)
        self.menuAccount.addSeparator()
        self.menuAccount.addAction(self.actionLog_Out)
        self.menubar.addAction(self.menuAccount.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addtarget_Button.setText(_translate("MainWindow", "+"))
        self.Archive_button.setText(_translate("MainWindow", "Archive"))
        self.Tema_button.setText(_translate("MainWindow", "☼"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuAccount.setTitle(_translate("MainWindow", "Account"))
        self.Createtarget_action.setText(_translate("MainWindow", "Создать цель"))
        self.actionLogin.setText(_translate("MainWindow", "Login"))
        self.actionLog_Out.setText(_translate("MainWindow", "Log Out"))
        self.Save_CSV_action.setText(_translate("MainWindow", "Сохранить CSV"))
        self.menubar.setStyleSheet("""
            QMenuBar {
                background-color: rgb(240,240,240);
                color: rgb(0,0,0);
                border: 1px solid ;
            }

            QMenuBar::item {
                background-color: rgb(240,240,240);
                color: rgb(0,0,0);
            }

            QMenuBar::item::selected {
                background-color: rgb(255,255,255);
                color: rgb(0, 0, 0)
            }
            QMenu {
                background-color: rgb(255,255,255);
                color: rgb(0,0,0);
                border: 1px solid ;
            }

            QMenu::item {
                background-color: rgb(255,255,255);
                color: rgb(0,0,0);
            }

            QMenu::item::selected {
                background-color: rgb(240,240,240);
                color: rgb(0, 0, 0)
            }
        """)


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.logins = ''
        self.idowner = ''
        self.setupUi(self)
        self.addtarget_Button.clicked.connect(self.createtarget)
        self.Tema_button.clicked.connect(self.changing_the_topic)
        self.Archive_button.clicked.connect(self.archive)
        self.actionLogin.triggered.connect(self.login_windows)
        self.actionLog_Out.triggered.connect(self.unlogin)
        self.Createtarget_action.triggered.connect(self.createtarget)
        self.Save_CSV_action.triggered.connect(self.save_csv)
        self.con = sqlite3.connect("account.db")
        self.Temawhite = True
        self.targetTable.itemChanged.connect(self.item_changed)
        self.modified = {}
        self.titles = None
        self.Telegram_button.clicked.connect(self.bind_telegram)

    def login_windows(self):
        if self.idowner == '':
            self.log_window = Logins_Register()
            self.log_window.closelog.connect(self.dialog_signal_slot)
            self.log_window.show()
            self.log_window.Tema(self.Temawhite)
        else:
            QMessageBox.critical(self, "Ошибка ", "Вы уже зашли в аккаунт", QMessageBox.Ok)

    def unlogin(self):
        if self.idowner == '':
            QMessageBox.critical(self, "Ошибка ", "Невозможно выйти из аккаунта", QMessageBox.Ok)
        else:
            self.con.commit()
            self.logins, self.idowner = '', ''
            self.hello_label.setText('Войдите в аккаунт')
            self.targetTable.setRowCount(0)
            self.targetTable.setColumnCount(0)

    def update_telegram_status(self, is_bound, username=""):
        if is_bound:
            self.Telegram_button.setText(f"TG: @{username}")
        else:
            self.Telegram_button.setText("Привязать TG")

    def bind_telegram(self):
        if self.idowner == '':
            QMessageBox.critical(self, "Ошибка", "Вы не зашли в аккаунт")
            return

        is_bound, username = check_binding_status(self.idowner)
        if is_bound:
            reply = QMessageBox.question(self, "Telegram", f"Аккаунт привязан к @{username}\nОтвязать?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                cur = self.con.cursor()
                cur.execute("DELETE FROM telegram_connections WHERE owner_id = ?", (self.idowner,))
                self.con.commit()
                self.update_telegram_status(False)
            return

        self.telegram_binding_window = TelegramBindingWindow(self.idowner, self)
        self.telegram_binding_window.show()
        self.telegram_binding_window.Tema(self.Temawhite)

    def dialog_signal_slot(self):
        self.logins, self.idowner = self.log_window.logins, self.log_window.idowner
        if len(self.logins) <= 12 and self.logins != '':
            self.hello_label.setText(f'Привет, {self.logins}.')
        elif len(self.logins) > 12:
            self.hello_label.setText(f'Здравствуйте, Mr.длин.')
        if self.logins != '':
            self.Update()
            is_bound, username = check_binding_status(self.idowner)
            if is_bound:
                self.update_telegram_status(True, username)

    def createtarget(self):
        if self.idowner == '':
            QMessageBox.critical(self, "Ошибка ", "Вы не зашли в аккаунт", QMessageBox.Ok)
        else:
            self.create_window = CreateTarget(self)
            self.create_window.ownerID = self.idowner
            self.create_window.show()
            self.create_window.Tema(self.Temawhite)

    def item_changed(self, item):
        if item.column() in [1, 3, 4]:
            return

        if self.targetTable.currentRow() != -1 and self.titles:
            if item.column() == 0:
                self.modified[self.titles[item.column()]] = item.text()
                self.Save()

    def Save(self):
        if not self.modified:
            return

        current_row = self.targetTable.currentRow()
        if current_row == -1:
            self.modified.clear()
            return

        cur = self.con.cursor()
        target_id = self.result_id[current_row][0]

        for key, value in self.modified.items():
            if key == 'Name':
                cur.execute('UPDATE target SET Name = ? WHERE idtarget = ?', (value, target_id))

        self.con.commit()
        self.modified.clear()

    def Ready(self):
        cur = self.con.cursor()
        cur = cur.execute('UPDATE target SET Ready = ? WHERE idtarget = ?', (
            1, self.result_id[self.targetTable.currentRow()][0])).fetchall()
        self.con.commit()
        self.Update()

    def Delete(self):
        current_row = self.targetTable.currentRow()
        if current_row < 0:
            return

        valid = QMessageBox.question(
            self, '', "Вы действительно хотите удалить задачу?",
            QMessageBox.Yes, QMessageBox.No)

        if valid == QMessageBox.Yes:
            cur = self.con.cursor()
            cur.execute('UPDATE target SET isDelete = ? WHERE idtarget = ?', (1, self.result_id[current_row][0]))
            self.con.commit()
            self.Update()
        else:
            qcheck = QCheckBox()
            qcheck.setChecked(False)
            qcheck.setEnabled(True)
            qcheck.toggled.connect(self.Delete)
            self.targetTable.setCellWidget(current_row, 4, qcheck)

    def Update(self):
        cur = self.con.cursor()
        result = cur.execute(
            "SELECT Name, priority, Time,"
            " Ready, isDelete FROM target WHERE ownerID=? AND Ready = ? AND isDelete = ?",
            (self.idowner, 0, 0,)).fetchall()
        if result:
            self.result_id = cur.execute(
                "SELECT target.idtarget FROM target INNER JOIN priority ON target.Priority = priority.id WHERE ownerID=? AND Ready = ? AND isDelete = ?",
                (self.idowner, 0, 0,)).fetchall()
            self.titles = [description[0] for description in cur.description]
            self.targetTable.setRowCount(len(result))
            self.targetTable.setColumnCount(len(result[0]))
            for i, elem in enumerate(result):
                for j, val in enumerate(elem):
                    if j == 1:
                        qcombo = QComboBox()
                        qcombo.addItems(['Менее важно', 'Важно', 'Очень важно', 'Абсолютно важно!!!'])
                        qcombo.setCurrentIndex(int(val) - 1)
                        qcombo.currentTextChanged.connect(self.change_priority)
                        self.targetTable.setCellWidget(i, j, qcombo)
                    elif j == 2:
                        item = QTableWidgetItem(val)
                        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                        self.targetTable.setItem(i, j, item)
                    elif j > 2:
                        qcheck = QCheckBox()
                        qcheck.setChecked(booling[val])
                        if j == 3:
                            qcheck.toggled.connect(self.Ready)
                        elif j == 4:
                            qcheck.toggled.connect(self.Delete)
                        self.targetTable.setCellWidget(i, j, qcheck)
                    else:
                        self.targetTable.setItem(i, j, QTableWidgetItem(str(val)))
            self.modified = {}
            self.targetTable.setHorizontalHeaderLabels(['Название', 'Приоритет', 'Время', 'Выполнено', 'Удалить'])
        else:
            self.targetTable.setRowCount(0)
            self.targetTable.setColumnCount(0)

    def changing_the_topic(self):
        if self.Temawhite:
            self.Temawhite = False
            self.actionLogin.text()
            self.setStyleSheet('background-color: rgb(49, 49, 49)')
            self.Tema_button.setStyleSheet('color: white')
            self.Archive_button.setStyleSheet('color: white')
            self.addtarget_Button.setStyleSheet('color: white')
            self.hello_label.setStyleSheet('color: white')
            self.menubar.setStyleSheet("""
                        QMenuBar {
                            background-color: rgb(49,49,49);
                            color: rgb(255,255,255);
                            border: 1px solid ;
                        }

                        QMenuBar::item {
                            background-color: rgb(49,49,49);
                            color: rgb(255,255,255);
                        }

                        QMenuBar::item::selected {
                            background-color: rgb(25,25,25);
                            color: rgb(255, 255, 255)
                        }
                        QMenu {
                            background-color: rgb(49,49,49);
                            color: rgb(255,255,255);
                            border: 1px solid ;
                        }

                        QMenu::item {
                            background-color: rgb(49,49,49);
                            color: rgb(255,255,255);
                        }

                        QMenu::item::selected {
                            background-color: rgb(25,25,25);
                            color: rgb(255, 255, 255)
                        }
                    """)
        else:
            self.Temawhite = True
            self.setStyleSheet('background-color: rgb(255, 255, 255)')
            self.Tema_button.setStyleSheet('color: black')
            self.Archive_button.setStyleSheet('color: black')
            self.addtarget_Button.setStyleSheet('color: black')
            self.hello_label.setStyleSheet('color: black')
            self.menubar.setStyleSheet("""
                        QMenuBar {
                            background-color: rgb(240,240,240);
                            color: rgb(0,0,0);
                            border: 1px solid ;
                        }

                        QMenuBar::item {
                            background-color: rgb(240,240,240);
                            color: rgb(0,0,0);
                        }

                        QMenuBar::item::selected {
                            background-color: rgb(255,255,255);
                            color: rgb(0, 0, 0)
                        }
                        QMenu {
                            background-color: rgb(255,255,255);
                            color: rgb(0,0,0);
                            border: 1px solid ;
                        }

                        QMenu::item {
                            background-color: rgb(255,255,255);
                            color: rgb(0,0,0);
                        }

                        QMenu::item::selected {
                            background-color: rgb(240,240,240);
                            color: rgb(0, 0, 0)
                        }
                    """)

    def archive(self):
        if self.idowner == '':
            QMessageBox.critical(self, "Ошибка ", "Вы не зашли в аккаунт", QMessageBox.Ok)
        else:
            self.archive_table = Archive()
            self.archive_table.ownerid = self.idowner
            self.archive_table.show()
            self.archive_table.table()
            self.archive_table.Tema(self.Temawhite)

    def change_priority(self, item):
        current_row = self.targetTable.currentRow()
        if current_row == -1:
            return
        target_id = self.result_id[current_row][0]
        cur = self.con.cursor()
        cur.execute('UPDATE target SET Priority = ? WHERE idtarget = ?',
                    (Combo[item], target_id))
        self.con.commit()

    def save_csv(self):
        if self.idowner == '':
            QMessageBox.critical(self, "Ошибка ", "Вы не зашли в аккаунт", QMessageBox.Ok)
        else:
            cur = self.con
            result = cur.execute(
                "SELECT target.Name, priority.title, target.Time FROM target INNER JOIN priority ON target.Priority = priority.id WHERE ownerID=? AND Ready = ? AND isDelete = ?",
                (self.idowner, 0, 0,)).fetchall()

            with open('results.csv', 'w', newline='') as csvfile:
                writer = csv.writer(
                    csvfile, delimiter=';', quotechar='"',
                    quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    [self.targetTable.horizontalHeaderItem(i).text()
                     for i in range(self.targetTable.columnCount() - 2)])
                for i in range(len(result)):
                    row = []
                    for j in range(len(result[i])):
                        item = result[i][j]
                        row.append(item)
                    writer.writerow(row)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
