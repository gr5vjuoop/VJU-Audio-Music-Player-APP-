from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl, QTimer, Qt
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from add_function import Add

import os, datetime, random


class Play(Add, QMainWindow):
    def __init__(self, song_list):
        super().__init__()
        uic.loadUi("Gui/playscreen.ui", self)
        self.setWindowIcon(QtGui.QIcon("Images/icon.jpg"))
        self.setWindowTitle('VJU Audio')

        self.current_songs = song_list

        self.repeat_status = False
        self.is_playing = False

        self.musicPlaying.hide()

        #Kết nối nút bấm
        self.Slider.sliderMoved[int].connect(lambda: self.player.setPosition(self.Slider.value()))
        self.playButton1.clicked.connect(self.play_song)
        self.pauseButton.clicked.connect(self.pause_and_unpause)
        self.nextButton.clicked.connect(self.next_song)
        self.preButton.clicked.connect(self.previous_song)
        self.backButton1.clicked.connect(self.stop)
        self.shuffleButton.clicked.connect(self.shuffle_songs)
        self.repeat.clicked.connect(self.toggle_repeat)

        #Tạo thời gian
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.move_slider)
        self.timer.timeout.connect(self.update_time)
        self.timer.timeout.connect(self.check_song_finished)

        # Lấy tham chiếu đến volumeSlider từ file .ui
        self.volumeSlider = self.findChild(QSlider, "volumeSlider") 
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setValue(100)  # Giá trị âm lượng ban đầu
        self.volumeSlider.valueChanged.connect(self.change_volume)
        
    def create_playing_list(self):
        #Sao chép danh sách nhạc sang danh sách mới
        playlist = self.current_songs.copy()
        
        for song in playlist:
            self.musicPlaying.addItem(os.path.basename(song))


    #Phát nhạc
    def play_song(self):

        if not self.current_songs:
            # Nếu danh sách bài hát trống, không thực hiện gì cả
            return

        current_selection = self.musicPlaying.currentRow()
        if current_selection == 0:
            current_selection = 1  # Chỉnh thành bài hát đầu tiên nếu chưa có bài hát nào được chọn

        current_selection = self.musicPlaying.currentRow()
        current_song = self.current_songs[current_selection]

        # Hiển thị tên bài hát đang phát
        self.CurrentSong.setText(os.path.basename(current_song))
        self.CurrentSong.setAlignment(Qt.AlignCenter)

        #Thêm nhạc 
        self.create_playing_list()
        
        #Phát bài hát
        song_url = QMediaContent(QUrl.fromLocalFile(current_song))
        self.player.setMedia(song_url)
        self.is_playing = True
        self.player.play()
        self.move_slider()

    #Chỉnh âm lượng
    def change_volume(self, value):
        self.player.setVolume(value)

    #Kiểm tra xem bài hiện tại đã kết thúc hay chưa
    def check_song_finished(self):
        if self.is_playing and self.player.mediaStatus() == QMediaPlayer.EndOfMedia:
            #Tự động chuyển sang bài kế tiếp
            self.auto_next()

    def toggle_repeat(self):
        # Đảo ngược trạng thái của nút lặp
        self.repeat_status = not self.repeat_status
        if self.repeat_status:
            rpbtn1 = QtGui.QIcon()
            rpbtn1.addPixmap(QtGui.QPixmap("Images/repeatbtn1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.repeat.setIcon(rpbtn1)
        else:
            rpbtn2 = QtGui.QIcon()
            rpbtn2.addPixmap(QtGui.QPixmap("Images/repeatbtn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.repeat.setIcon(rpbtn2)

    #Tự động chuyển bài tiếp theo nếu bài hiện tại đã kết thúc
    def auto_next(self):
        if self.player.mediaStatus() == QMediaPlayer.EndOfMedia:
            if self.repeat_status:
                # Nếu đang ở trạng thái lặp, chơi lại bài hát hiện tại   
                self.player.play()
            else:
                # Nếu không, chuyển sang bài hát tiếp theo
                self.next_song()



    #Di chuyển thanh tua nhạc
    def move_slider(self):
        #Kiểm tra nếu bài hát đang được phát
        if self.player.state() == QMediaPlayer.PlayingState:
            self.Slider.setMinimum(0)
            self.Slider.setMaximum(self.player.duration())
            self.slider_position = self.player.position()
            self.Slider.setValue(self.slider_position)

    def update_time(self):
    #Kiểm tra nếu bài hát đang được phát
        if self.player.state() == QMediaPlayer.PlayingState:
            #Cập nhật thời gian - thời lượng
            current_time = datetime.timedelta(seconds=self.player.position() // 1000)
            song_duration = datetime.timedelta(seconds=self.player.duration() // 1000)
            self.start_time.setText(str(current_time))
            self.end_time.setText(str(song_duration))

    #Tạm dừng nhạc
    def pause_and_unpause(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            pause = QtGui.QIcon()
            pause.addPixmap(QtGui.QPixmap("Images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pauseButton.setIcon(pause)
        else:
            self.player.play()
            self.is_playing = True
            play = QtGui.QIcon()
            play.addPixmap(QtGui.QPixmap("Images/pausebtn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pauseButton.setIcon(play)

    #Chuyển bài tiếp theo
    def next_song(self):

        if not self.current_songs:
            # Nếu danh sách bài hát trống, không thực hiện gì cả
            return

        try:
            current_selection = self.musicPlaying.currentRow()

            if current_selection+1 == len(self.current_songs):
                next_index = 0
            else:
                next_index = current_selection +1

            current_song = self.current_songs[next_index]
            self.musicPlaying.setCurrentRow(next_index)

            self.CurrentSong.setText(os.path.basename(current_song))
            self.CurrentSong.setAlignment(Qt.AlignCenter)

            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Next song error: {e}")

    # Chuyển bài trước đó
    def previous_song(self):
        try:
            current_selection = self.musicPlaying.currentRow()

            if current_selection == 0:
                previous_index = len(self.current_songs) - 1
            else:
                previous_index = current_selection - 1

            current_song = self.current_songs[previous_index]
            self.musicPlaying.setCurrentRow(previous_index)

            self.CurrentSong.setText(os.path.basename(current_song))
            self.CurrentSong.setAlignment(Qt.AlignCenter)

            song_url = QMediaContent(QUrl.fromLocalFile(current_song))
            self.player.setMedia(song_url)
            self.player.play()
            self.move_slider()
        except Exception as e:
            print(f"Previous song error: {e}")    

    #Dừng nhạc khi bấm nút Back
    def stop(self):
        self.player.stop()
        self.is_playing = False

    def shuffle_songs(self):
        random.shuffle(self.current_songs)
        self.create_playing_list()
