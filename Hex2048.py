# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Hex2048.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(751, 815)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.QuitButton = QPushButton(self.centralwidget)
        self.QuitButton.setObjectName(u"QuitButton")
        self.QuitButton.setGeometry(QRect(5, 90, 101, 31))
        self.NewButton = QPushButton(self.centralwidget)
        self.NewButton.setObjectName(u"NewButton")
        self.NewButton.setGeometry(QRect(5, 10, 101, 31))
        self.ControlButtons = QGroupBox(self.centralwidget)
        self.ControlButtons.setObjectName(u"ControlButtons")
        self.ControlButtons.setGeometry(QRect(230, 520, 281, 251))
        self.ControlButtons.setFlat(False)
        self.ControlButtons.setCheckable(False)
        self.TLButton = QPushButton(self.ControlButtons)
        self.TLButton.setObjectName(u"TLButton")
        self.TLButton.setGeometry(QRect(30, 60, 101, 41))
        self.TRButton = QPushButton(self.ControlButtons)
        self.TRButton.setObjectName(u"TRButton")
        self.TRButton.setGeometry(QRect(140, 60, 101, 41))
        self.LButton = QPushButton(self.ControlButtons)
        self.LButton.setObjectName(u"LButton")
        self.LButton.setGeometry(QRect(10, 110, 101, 41))
        self.RButton = QPushButton(self.ControlButtons)
        self.RButton.setObjectName(u"RButton")
        self.RButton.setGeometry(QRect(160, 110, 101, 41))
        self.BLButton = QPushButton(self.ControlButtons)
        self.BLButton.setObjectName(u"BLButton")
        self.BLButton.setGeometry(QRect(30, 160, 101, 41))
        self.BRButton = QPushButton(self.ControlButtons)
        self.BRButton.setObjectName(u"BRButton")
        self.BRButton.setGeometry(QRect(140, 160, 101, 41))
        self.Label_Text = QLabel(self.ControlButtons)
        self.Label_Text.setObjectName(u"Label_Text")
        self.Label_Text.setGeometry(QRect(100, 10, 71, 31))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(11)
        self.Label_Text.setFont(font)
        self.Label_Text.setLineWidth(2)
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(110, 50, 521, 461))
        self.Label_player = QLabel(self.centralwidget)
        self.Label_player.setObjectName(u"Label_player")
        self.Label_player.setGeometry(QRect(640, 10, 51, 31))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(12)
        self.Label_player.setFont(font1)
        self.Label_Text_Player = QLabel(self.centralwidget)
        self.Label_Text_Player.setObjectName(u"Label_Text_Player")
        self.Label_Text_Player.setGeometry(QRect(580, 10, 61, 31))
        self.Label_Text_Player.setFont(font)
        self.Label_Text_Player.setAlignment(Qt.AlignCenter)
        self.SaveGameButton = QPushButton(self.centralwidget)
        self.SaveGameButton.setObjectName(u"SaveGameButton")
        self.SaveGameButton.setGeometry(QRect(115, 10, 101, 31))
        self.LoadButton = QPushButton(self.centralwidget)
        self.LoadButton.setObjectName(u"LoadButton")
        self.LoadButton.setGeometry(QRect(225, 10, 101, 31))
        self.AIButton = QPushButton(self.centralwidget)
        self.AIButton.setObjectName(u"AIButton")
        self.AIButton.setGeometry(QRect(5, 50, 101, 31))
        MainWindow.setCentralWidget(self.centralwidget)
        self.graphicsView.raise_()
        self.QuitButton.raise_()
        self.NewButton.raise_()
        self.ControlButtons.raise_()
        self.Label_player.raise_()
        self.Label_Text_Player.raise_()
        self.SaveGameButton.raise_()
        self.LoadButton.raise_()
        self.AIButton.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 751, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.QuitButton.setText(QCoreApplication.translate("MainWindow", u"Quit", None))
        self.NewButton.setText(QCoreApplication.translate("MainWindow", u"New Game", None))
        self.ControlButtons.setTitle("")
        self.TLButton.setText(QCoreApplication.translate("MainWindow", u"Top - Left", None))
        self.TRButton.setText(QCoreApplication.translate("MainWindow", u"Top - Right", None))
        self.LButton.setText(QCoreApplication.translate("MainWindow", u"Left", None))
        self.RButton.setText(QCoreApplication.translate("MainWindow", u"Right", None))
        self.BLButton.setText(QCoreApplication.translate("MainWindow", u"Bottom - left", None))
        self.BRButton.setText(QCoreApplication.translate("MainWindow", u"Botton - Right", None))
        self.Label_Text.setText(QCoreApplication.translate("MainWindow", u"Controls", None))
        self.Label_player.setText("")
        self.Label_Text_Player.setText(QCoreApplication.translate("MainWindow", u"Player :", None))
        self.SaveGameButton.setText(QCoreApplication.translate("MainWindow", u"Save Game", None))
        self.LoadButton.setText(QCoreApplication.translate("MainWindow", u"Load Game", None))
        self.AIButton.setText(QCoreApplication.translate("MainWindow", u"Play with AI", None))
    # retranslateUi

