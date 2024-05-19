from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic, QtGui
import json, os

class Register(QMainWindow):
    register_success = pyqtSignal()
    def __init__(self):
            super().__init__()
            uic.loadUi("Gui/register.ui", self)

            self.setWindowIcon(QtGui.QIcon("Images/icon.jpg"))
            self.setWindowTitle('VJU Audio')
            self.registerbtn.clicked.connect(self.register_user)

    def show_message(self, title, message, icon=QMessageBox.Information):
        msg_box = QMessageBox()
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec_()

    def register_user(self):
        username = self.Username.text()
        password = self.Password.text()
        email = self.Email.text()

        if not username or not password or not email:
            self.show_message("Error", "All fields are required.", QMessageBox.Warning)
            return

        user_data = {"username": username, "password": password, "email": email}

        if os.path.exists("users.json"):
            with open("users.json", "r") as file:
                users = json.load(file)
        else:
            users = []

        for user in users:
            if user["username"] == username:
                self.show_message("Error", "Username already exists.", QMessageBox.Warning)
                return

        users.append(user_data)

        with open("users.json", "w") as file:
            json.dump(users, file)

        self.show_message("Success", "Registration successful.", QMessageBox.Information)
        self.register_success.emit()  # Emit success signal
        self.close()