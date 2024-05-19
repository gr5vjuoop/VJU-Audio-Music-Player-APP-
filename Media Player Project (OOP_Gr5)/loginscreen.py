from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic, QtGui
import json, os

class Login(QMainWindow):
    signin_successful = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        uic.loadUi("Gui/login.ui", self)

        self.setWindowIcon(QtGui.QIcon("Images/icon.jpg"))
        self.setWindowTitle('VJU Audio')
        self.loginbutton.clicked.connect(self.login_user)
        self.Username.returnPressed.connect(self.login_user)
        self.Password.returnPressed.connect(self.login_user)

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def login_user(self):
        username = self.Username.text()
        password = self.Password.text()

        if not username or not password:
            self.show_message("Error", "All fields are required.", QMessageBox.Warning)
            return

        if not os.path.exists("users.json"):
            self.show_message("Error", "No users found. Please register first.", QMessageBox.Warning)
            return

        with open("users.json", "r") as file:
            users = json.load(file)

        for user in users:
            if user["username"] == username and user["password"] == password:
                self.show_message("Success", f"Welcome {username}!", QMessageBox.Information)
                self.signin_successful.emit(username)  # Phát tín hiệu khi đăng nhập thành công
                return

        self.show_message("Error", "Invalid username or password.", QMessageBox.Warning)
