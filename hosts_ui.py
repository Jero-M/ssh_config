# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hosts.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(517, 346)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(12)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(10)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.list_hosts = QtGui.QListWidget(self.centralwidget)
        self.list_hosts.setObjectName(_fromUtf8("list_hosts"))
        self.gridLayout.addWidget(self.list_hosts, 0, 0, 6, 1)
        self.button_remove = QtGui.QPushButton(self.centralwidget)
        self.button_remove.setObjectName(_fromUtf8("button_remove"))
        self.gridLayout.addWidget(self.button_remove, 1, 1, 1, 1)
        self.button_load = QtGui.QPushButton(self.centralwidget)
        self.button_load.setObjectName(_fromUtf8("button_load"))
        self.gridLayout.addWidget(self.button_load, 0, 1, 1, 1)
        self.text_host = QtGui.QLineEdit(self.centralwidget)
        self.text_host.setObjectName(_fromUtf8("text_host"))
        self.gridLayout.addWidget(self.text_host, 2, 1, 1, 1)
        self.button_add = QtGui.QPushButton(self.centralwidget)
        self.button_add.setObjectName(_fromUtf8("button_add"))
        self.gridLayout.addWidget(self.button_add, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.list_hosts.setSortingEnabled(False)
        self.button_remove.setText(_translate("MainWindow", "Remove Selected", None))
        self.button_load.setText(_translate("MainWindow", "Load Hosts List", None))
        self.button_add.setText(_translate("MainWindow", "Add Host", None))
