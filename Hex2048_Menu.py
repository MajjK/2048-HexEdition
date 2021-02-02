# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Hex2048_Menu.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_StartWindow(object):
    def setupUi(self, StartWindow):
        if not StartWindow.objectName():
            StartWindow.setObjectName(u"StartWindow")
        StartWindow.resize(251, 268)
        StartWindow.setStyleSheet(u"background-color: rgb(251, 255, 243);\n"
"border-color: rgb(185, 163, 126);")
        self.centralwidget = QWidget(StartWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.new_button = QPushButton(self.centralwidget)
        self.new_button.setObjectName(u"new_button")
        self.new_button.setGeometry(QRect(70, 50, 101, 31))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.new_button.setFont(font)
        self.new_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.ai_button = QPushButton(self.centralwidget)
        self.ai_button.setObjectName(u"ai_button")
        self.ai_button.setGeometry(QRect(70, 90, 101, 31))
        self.ai_button.setFont(font)
        self.ai_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.load_button = QPushButton(self.centralwidget)
        self.load_button.setObjectName(u"load_button")
        self.load_button.setGeometry(QRect(70, 130, 101, 31))
        self.load_button.setFont(font)
        self.load_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.scores_button = QPushButton(self.centralwidget)
        self.scores_button.setObjectName(u"scores_button")
        self.scores_button.setGeometry(QRect(70, 170, 101, 31))
        self.scores_button.setFont(font)
        self.scores_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.quit_button = QPushButton(self.centralwidget)
        self.quit_button.setObjectName(u"quit_button")
        self.quit_button.setGeometry(QRect(70, 210, 101, 31))
        self.quit_button.setFont(font)
        self.quit_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.nick_edit = QTextEdit(self.centralwidget)
        self.nick_edit.setObjectName(u"nick_edit")
        self.nick_edit.setGeometry(QRect(110, 10, 111, 31))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.nick_edit.setFont(font1)
        self.nick_edit.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.label_text_nickname = QLabel(self.centralwidget)
        self.label_text_nickname.setObjectName(u"label_text_nickname")
        self.label_text_nickname.setGeometry(QRect(20, 10, 81, 31))
        self.label_text_nickname.setFont(font1)
        self.label_text_nickname.setAlignment(Qt.AlignCenter)
        StartWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(StartWindow)
        self.statusbar.setObjectName(u"statusbar")
        StartWindow.setStatusBar(self.statusbar)

        self.retranslateUi(StartWindow)

        QMetaObject.connectSlotsByName(StartWindow)
    # setupUi

    def retranslateUi(self, StartWindow):
        StartWindow.setWindowTitle(QCoreApplication.translate("StartWindow", u"MainWindow", None))
        self.new_button.setText(QCoreApplication.translate("StartWindow", u"New Game", None))
        self.ai_button.setText(QCoreApplication.translate("StartWindow", u"Play with AI", None))
        self.load_button.setText(QCoreApplication.translate("StartWindow", u"Load Game", None))
        self.scores_button.setText(QCoreApplication.translate("StartWindow", u"Scores", None))
        self.quit_button.setText(QCoreApplication.translate("StartWindow", u"Quit", None))
        self.nick_edit.setPlaceholderText(QCoreApplication.translate("StartWindow", u"User", None))
        self.label_text_nickname.setText(QCoreApplication.translate("StartWindow", u"Nickname", None))
    # retranslateUi

