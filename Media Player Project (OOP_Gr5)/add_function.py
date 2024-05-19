from PyQt5 import QtWidgets, QtMultimedia, uic, QtGui
from PyQt5.QtWidgets import *
import os

class Add(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Gui/add.ui", self)
        self.setWindowIcon(QtGui.QIcon("Images/icon.jpg"))
        self.setWindowTitle('VJU Audio')

        self.current_songs = []

        self.player = QtMultimedia.QMediaPlayer()
    
        self.actionAdd_Songs.triggered.connect(self.add_songs)
        self.actionRemove_Selected_Song.triggered.connect(self.remove_selected_song)
        self.actionRemove_All_Song.triggered.connect(self.remove_all_song)

    #set username
    def set_username(self, username):
        self.name.setText(f"{username}")    

    #Thêm bài hát
    def add_songs(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(
        self, caption="Add Music",
        directory=':\\', filter="Supported Files (*.mp3; *.m4a; *.wma)"
        )
        if files:
            for file in files:
                self.current_songs.append(file)
                self.MusicLists.addItem(os.path.basename(file))

        global songlist 
        songlist = self.current_songs


    #Xoá bài nhạc được chọn
    def remove_selected_song(self):
        current_selection = self.MusicLists.currentRow()
        self.current_songs.pop(current_selection)
        self.MusicLists.takeItem(current_selection)

    #Xoá tất cả các bài hát
    def remove_all_song(self):
        self.MusicLists.clear()
        self.current_songs.clear()