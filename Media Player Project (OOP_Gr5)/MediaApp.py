from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtWidgets

from loginscreen import Login
from add_function import Add
from playscreen import Play
from register import Register

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.login = Login()
        self.add = Add()
        self.play = Play(self.add.current_songs)
        self.register = Register()

        self.login.show()
        self.login.signin_successful.connect(self.login_successful)
        self.register.register_success.connect(self.show_login)

        self.login.createbtn.clicked.connect(lambda: self.changeCS("create"))
        self.add.backButton.clicked.connect(lambda: self.changeCS("login"))
        self.add.playButton.clicked.connect(lambda: self.changeCS("play"))
        self.play.backButton1.clicked.connect(lambda: self.changeCS("add"))

    def handle_signal(self):
        self.add.play_signal.connect(self.play.play_song)

    def login_successful(self, username):
        self.add.set_username(username)
        self.login.hide()
        self.add.show()

    def show_register(self):
        self.login.hide()
        self.register.show()

    def show_login(self):
        self.register.hide()
        self.login.show()

    def changeCS(self, i):
        if i == "login":
            self.add.hide()
            self.login.show()
        elif i == "play":
            self.add.hide()
            self.play.show()
        elif i == "add":
            self.play.hide()
            self.add.show()
        elif i == "create":
            self.login.hide()
            self.register.show()


if __name__ == "__main__":
    app = QApplication([])
    ui = MainApp()
    app.exec_()