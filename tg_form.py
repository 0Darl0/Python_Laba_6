from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QMainWindow
from tg_bot import generate_binding_code, check_binding_status


class Ui_TelegramBinding(object):
    def setupUi(self, TelegramBinding):
        TelegramBinding.setObjectName("TelegramBinding")
        TelegramBinding.resize(400, 300)
        TelegramBinding.setStyleSheet("background-color: rgb(230, 255, 190);")

        self.title_label = QtWidgets.QLabel(TelegramBinding)
        self.title_label.setGeometry(QtCore.QRect(100, 20, 200, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setText("Привязка Telegram")

        self.info_label = QtWidgets.QLabel(TelegramBinding)
        self.info_label.setGeometry(QtCore.QRect(30, 70, 340, 60))
        self.info_label.setWordWrap(True)
        self.info_label.setAlignment(QtCore.Qt.AlignCenter)
        self.info_label.setText("1. Откройте Telegram\n2. Найдите бота\n3. Отправьте команду /code с кодом ниже")

        self.code_label = QtWidgets.QLabel(TelegramBinding)
        self.code_label.setGeometry(QtCore.QRect(50, 150, 300, 40))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        self.code_label.setFont(font)
        self.code_label.setAlignment(QtCore.Qt.AlignCenter)
        self.code_label.setStyleSheet("background-color: white; border: 2px solid black; border-radius: 5px;")

        self.status_label = QtWidgets.QLabel(TelegramBinding)
        self.status_label.setGeometry(QtCore.QRect(30, 210, 340, 30))
        self.status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.status_label.setText("Ожидание привязки...")

        self.close_button = QtWidgets.QPushButton(TelegramBinding)
        self.close_button.setGeometry(QtCore.QRect(150, 260, 100, 30))
        self.close_button.setText("Закрыть")


class TelegramBindingWindow(Ui_TelegramBinding, QMainWindow):
    def __init__(self, owner_id, parent=None):
        super().__init__()
        self.setupUi(self)
        self.owner_id = owner_id
        self.parent = parent

        self.binding_code = generate_binding_code(owner_id)
        self.code_label.setText(self.binding_code)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_status)
        self.timer.start(2000)

        self.close_button.clicked.connect(self.close)

    def check_status(self):
        is_bound, username = check_binding_status(self.owner_id)

        if is_bound:
            self.status_label.setText(f"Привязано! @{username}")
            self.status_label.setStyleSheet("color: green;")
            self.code_label.setText("ПРИВЯЗАНО")
            self.timer.stop()

            if self.parent:
                self.parent.update_telegram_status(True, username)

            QtCore.QTimer.singleShot(2000, self.close)

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

    def Tema(self, isWhite):
        if not isWhite:
            self.setStyleSheet('background-color: rgb(49, 49, 49)')
            self.title_label.setStyleSheet('color: white')
            self.info_label.setStyleSheet('color: white')
            self.code_label.setStyleSheet('background-color: #333; color: white; border: 2px solid white;')
            self.status_label.setStyleSheet('color: white')
            self.close_button.setStyleSheet('color: white')
        else:
            self.setStyleSheet('background-color: rgb(230, 255, 190)')
            self.title_label.setStyleSheet('color: black')
            self.info_label.setStyleSheet('color: black')
            self.code_label.setStyleSheet('background-color: white; color: black; border: 2px solid black;')
            self.status_label.setStyleSheet('color: black')
            self.close_button.setStyleSheet('color: black')