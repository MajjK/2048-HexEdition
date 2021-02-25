# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Hex2048_Multi.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MultiWindow(object):
    def setupUi(self, MultiWindow):
        if not MultiWindow.objectName():
            MultiWindow.setObjectName(u"MultiWindow")
        MultiWindow.resize(301, 141)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MultiWindow.sizePolicy().hasHeightForWidth())
        MultiWindow.setSizePolicy(sizePolicy)
        MultiWindow.setMaximumSize(QSize(301, 141))
        MultiWindow.setStyleSheet(u"background-color: rgb(251, 255, 243);\n"
"border-color: rgb(185, 163, 126);")
        self.centralwidget = QWidget(MultiWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.server_button = QPushButton(self.centralwidget)
        self.server_button.setObjectName(u"server_button")
        self.server_button.setGeometry(QRect(180, 50, 101, 31))
        font = QFont()
        font.setFamily(u"Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.server_button.setFont(font)
        self.server_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.port_edit = QTextEdit(self.centralwidget)
        self.port_edit.setObjectName(u"port_edit")
        self.port_edit.setGeometry(QRect(20, 10, 131, 35))
        font1 = QFont()
        font1.setFamily(u"Arial")
        font1.setPointSize(12)
        font1.setBold(True)
        font1.setWeight(75)
        self.port_edit.setFont(font1)
        self.port_edit.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.address_edit = QTextEdit(self.centralwidget)
        self.address_edit.setObjectName(u"address_edit")
        self.address_edit.setGeometry(QRect(20, 50, 131, 35))
        self.address_edit.setFont(font1)
        self.address_edit.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.connect_button = QPushButton(self.centralwidget)
        self.connect_button.setObjectName(u"connect_button")
        self.connect_button.setGeometry(QRect(180, 10, 101, 31))
        self.connect_button.setFont(font)
        self.connect_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        self.menu_button = QPushButton(self.centralwidget)
        self.menu_button.setObjectName(u"menu_button")
        self.menu_button.setGeometry(QRect(180, 90, 101, 31))
        self.menu_button.setFont(font)
        self.menu_button.setStyleSheet(u"background-color: rgb(197, 173, 134)")
        MultiWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MultiWindow)
        self.statusbar.setObjectName(u"statusbar")
        MultiWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MultiWindow)

        QMetaObject.connectSlotsByName(MultiWindow)
    # setupUi

    def retranslateUi(self, MultiWindow):
        MultiWindow.setWindowTitle(QCoreApplication.translate("MultiWindow", u"MainWindow", None))
        self.server_button.setText(QCoreApplication.translate("MultiWindow", u"Server", None))
        self.port_edit.setPlaceholderText(QCoreApplication.translate("MultiWindow", u"Port", None))
        self.address_edit.setPlaceholderText(QCoreApplication.translate("MultiWindow", u"IP Address", None))
        self.connect_button.setText(QCoreApplication.translate("MultiWindow", u"Connect", None))
        self.menu_button.setText(QCoreApplication.translate("MultiWindow", u"Menu", None))
    # retranslateUi

