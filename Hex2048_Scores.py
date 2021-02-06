# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Hex2048_Scores.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_ScoresWindow(object):
    def setupUi(self, ScoresWindow):
        if not ScoresWindow.objectName():
            ScoresWindow.setObjectName(u"ScoresWindow")
        ScoresWindow.resize(237, 390)
        ScoresWindow.setStyleSheet(u"background-color: rgb(251, 255, 243);\n"
"border-color: rgb(185, 163, 126);")
        self.centralwidget = QWidget(ScoresWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.scoreboard_text = QLabel(self.centralwidget)
        self.scoreboard_text.setObjectName(u"scoreboard_text")
        self.scoreboard_text.setGeometry(QRect(60, 5, 121, 31))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.scoreboard_text.setFont(font)
        self.scoreboard_text.setLineWidth(2)
        self.nickname_text = QLabel(self.centralwidget)
        self.nickname_text.setObjectName(u"nickname_text")
        self.nickname_text.setGeometry(QRect(20, 40, 81, 31))
        self.nickname_text.setFont(font)
        self.nickname_text.setLineWidth(2)
        self.score_text = QLabel(self.centralwidget)
        self.score_text.setObjectName(u"score_text")
        self.score_text.setGeometry(QRect(140, 40, 51, 31))
        self.score_text.setFont(font)
        self.score_text.setLineWidth(2)
        self.nick_text_edit = QPlainTextEdit(self.centralwidget)
        self.nick_text_edit.setObjectName(u"nick_text_edit")
        self.nick_text_edit.setGeometry(QRect(10, 70, 100, 291))
        self.nick_text_edit.setFont(font)
        self.score_text_edit = QPlainTextEdit(self.centralwidget)
        self.score_text_edit.setObjectName(u"score_text_edit")
        self.score_text_edit.setGeometry(QRect(120, 70, 100, 291))
        self.score_text_edit.setFont(font)
        ScoresWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(ScoresWindow)
        self.statusbar.setObjectName(u"statusbar")
        ScoresWindow.setStatusBar(self.statusbar)

        self.retranslateUi(ScoresWindow)

        QMetaObject.connectSlotsByName(ScoresWindow)
    # setupUi

    def retranslateUi(self, ScoresWindow):
        ScoresWindow.setWindowTitle(QCoreApplication.translate("ScoresWindow", u"MainWindow", None))
        self.scoreboard_text.setText(QCoreApplication.translate("ScoresWindow", u"SCOREBOARD", None))
        self.nickname_text.setText(QCoreApplication.translate("ScoresWindow", u"Nickname:", None))
        self.score_text.setText(QCoreApplication.translate("ScoresWindow", u"Score:", None))
    # retranslateUi

