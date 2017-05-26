# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'adcp_terminal.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AdcpTerminal(object):
    def setupUi(self, AdcpTerminal):
        AdcpTerminal.setObjectName("AdcpTerminal")
        AdcpTerminal.resize(687, 616)
        self.centralWidget = QtWidgets.QWidget(AdcpTerminal)
        self.centralWidget.setObjectName("centralWidget")
        self.terminalText = QtWidgets.QTextEdit(self.centralWidget)
        self.terminalText.setGeometry(QtCore.QRect(30, 30, 281, 141))
        self.terminalText.setObjectName("terminalText")
        self.breakButton = QtWidgets.QPushButton(self.centralWidget)
        self.breakButton.setGeometry(QtCore.QRect(242, 180, 81, 32))
        self.breakButton.setObjectName("breakButton")
        self.sendButton = QtWidgets.QPushButton(self.centralWidget)
        self.sendButton.setGeometry(QtCore.QRect(172, 180, 71, 32))
        self.sendButton.setObjectName("sendButton")
        self.cmdLineText = QtWidgets.QLineEdit(self.centralWidget)
        self.cmdLineText.setGeometry(QtCore.QRect(32, 180, 141, 21))
        self.cmdLineText.setObjectName("cmdLineText")
        AdcpTerminal.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(AdcpTerminal)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 687, 22))
        self.menuBar.setObjectName("menuBar")
        AdcpTerminal.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(AdcpTerminal)
        self.mainToolBar.setObjectName("mainToolBar")
        AdcpTerminal.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(AdcpTerminal)
        self.statusBar.setObjectName("statusBar")
        AdcpTerminal.setStatusBar(self.statusBar)

        self.retranslateUi(AdcpTerminal)
        QtCore.QMetaObject.connectSlotsByName(AdcpTerminal)

    def retranslateUi(self, AdcpTerminal):
        _translate = QtCore.QCoreApplication.translate
        AdcpTerminal.setWindowTitle(_translate("AdcpTerminal", "MainWindow"))
        self.breakButton.setText(_translate("AdcpTerminal", "BREAK"))
        self.sendButton.setText(_translate("AdcpTerminal", "SEND"))

