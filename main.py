import json
import os
import sys
import qdarkstyle
import pygame as pg

# from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from pygame import mixer,USEREVENT, event

play_song = []
loop = False
SONG_END = USEREVENT+1
SONG_REPEAT = USEREVENT+1

if not os.path.isfile('settings.json'):
    open('settings.json', 'a').close()
with open('settings.json','r') as jFile:
    jFile.seek(0)
    jdata = json.load(jFile)

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Music Player")
        MainWindow.resize(475, 380)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.song_progress = QtWidgets.QProgressBar(self.centralwidget)
        self.song_progress.setProperty("value", 0)
        self.song_progress.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.song_progress.setObjectName("song_progress")
        self.gridLayout_2.addWidget(self.song_progress, 1, 0, 1, 3)
        self.stop_but = QtWidgets.QPushButton(self.centralwidget)
        self.stop_but.setObjectName("stop_but")
        self.gridLayout_2.addWidget(self.stop_but, 0, 2, 1, 1)
        self.backward_b = QtWidgets.QPushButton(self.centralwidget)
        self.backward_b.setObjectName("backward")
        self.gridLayout_2.addWidget(self.backward_b, 0, 0, 1, 1)
        self.cont_pau = QtWidgets.QPushButton(self.centralwidget)
        self.cont_pau.setObjectName("cont_pau")
        self.gridLayout_2.addWidget(self.cont_pau, 0, 1, 1, 1)
        self.loop_single = QtWidgets.QCheckBox(self.centralwidget)
        self.loop_single.setObjectName("loop_single")
        self.gridLayout_2.addWidget(self.loop_single, 0, 4, 1, 1)
        self.forward_b = QtWidgets.QPushButton(self.centralwidget)
        self.forward_b.setObjectName("forward")
        self.gridLayout_2.addWidget(self.forward_b, 0, 3, 1, 1)
        self.time_remain = QtWidgets.QLabel(self.centralwidget)
        self.time_remain.setObjectName("time_remain")
        self.gridLayout_2.addWidget(self.time_remain, 1, 3, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.volume = QtWidgets.QLabel(self.centralwidget)
        self.volume.setAlignment(QtCore.Qt.AlignCenter)
        self.volume.setObjectName("volume")
        self.verticalLayout_2.addWidget(self.volume)
        self.volume_ctrl = QtWidgets.QSlider(self.centralwidget)
        self.volume_ctrl.setOrientation(QtCore.Qt.Horizontal)
        self.volume_ctrl.setObjectName("volume_ctrl")
        self.volume_ctrl.setValue(jdata["volume"])
        self.volume_ctrl.setMinimum(0)
        self.volume_ctrl.setMaximum(100)
        self.volume_ctrl.setSingleStep(1)
        self.verticalLayout_2.addWidget(self.volume_ctrl)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 1, 4, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.playing = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.playing.setFont(font)
        self.playing.setAlignment(QtCore.Qt.AlignCenter)
        self.playing.setObjectName("playing")
        self.verticalLayout.addWidget(self.playing)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 632, 25))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionLisence_Information = QtWidgets.QAction(MainWindow)
        self.actionLisence_Information.setObjectName("actionLisence_Information")
        self.menuFile.addAction(self.actionOpen)
        self.menuAbout.addAction(self.actionLisence_Information)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 5, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)
        self.event_timer = QTimer()
        self.info = QMessageBox()
        self.info.setWindowTitle("License Information")
        self.info.setText("MIT License\n\nCopyright (c) 2021 Marganotvke\n\nContact:")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.actionOpen.triggered.connect(lambda: self.open_file())
        self.actionLisence_Information.triggered.connect(lambda: self.license())
        self.cont_pau.clicked.connect(lambda: self.cur_playing())
        self.volume_ctrl.sliderMoved.connect(lambda: self.change_vol())
        self.volume_ctrl.sliderReleased.connect(lambda: self.vol_write())
        self.stop_but.clicked.connect(lambda: self.stop_playing())
        self.forward_b.clicked.connect(lambda: self.forward())
        self.backward_b.clicked.connect(lambda: self.backward())

        for e in event.get():
            if e.type == SONG_END:
                self.play_next()
            elif e.type == SONG_REPEAT:
                mixer.music.rewind()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Music Player"))
        self.song_progress.setFormat(_translate("MainWindow", "%p%"))
        self.stop_but.setText(_translate("MainWindow", "Stop"))
        self.backward_b.setText(_translate("MainWindow", "Backward"))
        self.cont_pau.setText(_translate("MainWindow", "Load Song"))
        self.loop_single.setText(_translate("MainWindow", "Loop"))
        self.forward_b.setText(_translate("MainWindow", "Forward"))
        self.time_remain.setText(_translate("MainWindow", "Time"))
        self.volume.setText(_translate("MainWindow", f"Volume: {jdata['volume']} "))
        self.playing.setText(_translate("MainWindow", "Currently Playing: None"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionLisence_Information.setText(_translate("MainWindow", "License Information"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))

    def license(self):
        self.info.exec_()

    def play_next(self):
        mixer.music.unload()
        play_song.pop(0)
        if play_song:
            mixer.music.load(play_song[0][1])
            self.playing.setText(f"Currently playing: {play_song[0][0]}")
            mixer.music.play()
        else:
            mixer.music.unload()
            self.playing.setText(f"Currently playing: None")

    def stop_playing(self):
        mixer.music.set_endevent()
        mixer.music.stop()
        mixer.music.unload()
        self.playing.setText(f"Currently playing: None")

    def cur_playing(self):
        if not play_song:
            self.open_file()
        else:
            if mixer.music.get_busy():
                mixer.music.pause()
                self.cont_pau.setText("Continue")
            else:
                mixer.music.unpause()
                self.cont_pau.setText("Pause")

    def forward(self):
        if play_song:
            mixer.music.stop()
            self.play_next()
        else:
            mixer.music.set_endevent()
            mixer.music.stop()
            mixer.music.unload()
            self.playing.setText(f"Currently playing: None")

    def backward(self):
        if play_song:
            mixer.music.rewind()
        else:
            pass

    def open_file(self):
        global play_song
        filename = QFileDialog.getOpenFileName(None, 'Open File', filter="*.mp3;;*.wav;;*.ogg;;All files(*)")
        if filename != ('', ''):
            song = os.path.basename(filename[0])
            play_song.append([song.split(".")[0],filename[0],int(mixer.Sound(filename[0]).get_length()*1000)])
            if not mixer.music.get_busy():
                mixer.music.load(play_song[0][1])
                self.playing.setText(f"Currently playing: {play_song[0][0]}")
                mixer.music.play()
            self.time_remain.setText(f"0/{int(play_song[0][2]/1000)}(s)")
            self.cont_pau.setText("Pause")
            self.event_timer.timeout.connect(self.handleTimer)
            self.event_timer.start(1000)

    def change_vol(self):
        vol = self.volume_ctrl.value()
        mixer.music.set_volume(vol/100)
        self.volume.setText(f"Volume: {vol}")

    def vol_write(self):
        vol = self.volume_ctrl.value()
        jdata["volume"] = vol
        mixer.music.set_volume(vol/100)
        self.volume.setText(f"Volume: {vol}")
        with open('settings.json', 'w') as jFile:
            json_string = json.dumps(jdata, default=lambda o: o.__dict__, sort_keys=True, indent=2)
            jFile.write(json_string)

    def handleTimer(self):
        if play_song:
            self.song_progress.setProperty("value",int((mixer.music.get_pos()/play_song[0][2])*100))
            self.time_remain.setText(f"{int(mixer.music.get_pos()/1000)}/{int(play_song[0][2]/1000)}(s)")
            if self.loop_single.isChecked():
                mixer.music.set_endevent(SONG_REPEAT)
            else:
                mixer.music.set_endevent(SONG_END)
        else:
            self.event_timer.stop()

if __name__ == "__main__":
    pg.init()
    mixer.music.set_volume(jdata["volume"])
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
