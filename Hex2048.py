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
        MainWindow.resize(560, 778)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        MainWindow.setStyleSheet(u"background-color: rgb(251, 255, 243);\n"
"border-color: rgb(185, 163, 126);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.ControlButtons = QGroupBox(self.centralwidget)
        self.ControlButtons.setObjectName(u"ControlButtons")
        self.ControlButtons.setGeometry(QRect(150, 530, 271, 221))
        self.ControlButtons.setFlat(False)
        self.ControlButtons.setCheckable(False)
        self.tl_button = QPushButton(self.ControlButtons)
        self.tl_button.setObjectName(u"tl_button")
        self.tl_button.setGeometry(QRect(30, 50, 101, 41))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.tl_button.setFont(font)
        self.tl_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.tr_button = QPushButton(self.ControlButtons)
        self.tr_button.setObjectName(u"tr_button")
        self.tr_button.setGeometry(QRect(140, 50, 101, 41))
        self.tr_button.setFont(font)
        self.tr_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.l_button = QPushButton(self.ControlButtons)
        self.l_button.setObjectName(u"l_button")
        self.l_button.setGeometry(QRect(10, 100, 101, 41))
        self.l_button.setFont(font)
        self.l_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.r_button = QPushButton(self.ControlButtons)
        self.r_button.setObjectName(u"r_button")
        self.r_button.setGeometry(QRect(160, 100, 101, 41))
        self.r_button.setFont(font)
        self.r_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.bl_button = QPushButton(self.ControlButtons)
        self.bl_button.setObjectName(u"bl_button")
        self.bl_button.setGeometry(QRect(30, 150, 101, 41))
        self.bl_button.setFont(font)
        self.bl_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.br_button = QPushButton(self.ControlButtons)
        self.br_button.setObjectName(u"br_button")
        self.br_button.setGeometry(QRect(140, 150, 101, 41))
        self.br_button.setFont(font)
        self.br_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.control_text = QLabel(self.ControlButtons)
        self.control_text.setObjectName(u"control_text")
        self.control_text.setGeometry(QRect(105, 10, 71, 31))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.control_text.setFont(font1)
        self.control_text.setLineWidth(2)
        self.graphics_view = QGraphicsView(self.centralwidget)
        self.graphics_view.setObjectName(u"graphics_view")
        self.graphics_view.setGeometry(QRect(20, 40, 521, 461))
        self.graphics_view.setAutoFillBackground(False)
        self.graphics_view.setStyleSheet(u"background: transparent\n"
"")
        self.graphics_view.setFrameShape(QFrame.NoFrame)
        self.graphics_view.setLineWidth(1)
        self.label_player = QLabel(self.centralwidget)
        self.label_player.setObjectName(u"label_player")
        self.label_player.setGeometry(QRect(480, 0, 71, 31))
        font2 = QFont()
        font2.setFamily(u"Arial")
        font2.setPointSize(12)
        font2.setBold(False)
        font2.setItalic(True)
        font2.setWeight(50)
        self.label_player.setFont(font2)
        self.label_text_player = QLabel(self.centralwidget)
        self.label_text_player.setObjectName(u"label_text_player")
        self.label_text_player.setGeometry(QRect(420, 0, 61, 31))
        self.label_text_player.setFont(font1)
        self.label_text_player.setAlignment(Qt.AlignCenter)
        self.save_game_button = QPushButton(self.centralwidget)
        self.save_game_button.setObjectName(u"save_game_button")
        self.save_game_button.setGeometry(QRect(120, 5, 101, 31))
        self.save_game_button.setFont(font)
        self.save_game_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.menu_button = QPushButton(self.centralwidget)
        self.menu_button.setObjectName(u"menu_button")
        self.menu_button.setGeometry(QRect(10, 5, 101, 31))
        self.menu_button.setFont(font)
        self.menu_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.label_color = QLabel(self.centralwidget)
        self.label_color.setObjectName(u"label_color")
        self.label_color.setGeometry(QRect(375, 0, 41, 31))
        self.label_color.setFont(font1)
        self.label_color.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.graphics_view.raise_()
        self.ControlButtons.raise_()
        self.label_player.raise_()
        self.label_text_player.raise_()
        self.save_game_button.raise_()
        self.menu_button.raise_()
        self.label_color.raise_()
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ControlButtons.setTitle("")
        self.tl_button.setText(QCoreApplication.translate("MainWindow", u"Top - Left", None))
        self.tr_button.setText(QCoreApplication.translate("MainWindow", u"Top - Right", None))
        self.l_button.setText(QCoreApplication.translate("MainWindow", u"Left", None))
        self.r_button.setText(QCoreApplication.translate("MainWindow", u"Right", None))
        self.bl_button.setText(QCoreApplication.translate("MainWindow", u"Bottom - left", None))
        self.br_button.setText(QCoreApplication.translate("MainWindow", u"Botton - Right", None))
        self.control_text.setText(QCoreApplication.translate("MainWindow", u"Controls", None))
        self.label_player.setText("")
        self.label_text_player.setText(QCoreApplication.translate("MainWindow", u"Player :", None))
        self.save_game_button.setText(QCoreApplication.translate("MainWindow", u"Save Game", None))
        self.menu_button.setText(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.label_color.setText("")
    # retranslateUi

