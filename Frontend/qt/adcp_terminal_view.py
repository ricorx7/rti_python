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
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(320, 30, 160, 111))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.serialPortcomboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.serialPortcomboBox.setObjectName("serialPortcomboBox")
        self.verticalLayout.addWidget(self.serialPortcomboBox)
        self.baudRatecomboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.baudRatecomboBox.setObjectName("baudRatecomboBox")
        self.verticalLayout.addWidget(self.baudRatecomboBox)
        self.serialConnectButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.serialConnectButton.setObjectName("serialConnectButton")
        self.verticalLayout.addWidget(self.serialConnectButton)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 180, 281, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cmdLineText = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.cmdLineText.setObjectName("cmdLineText")
        self.horizontalLayout.addWidget(self.cmdLineText)
        self.sendButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        self.breakButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.breakButton.setObjectName("breakButton")
        self.horizontalLayout.addWidget(self.breakButton)
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
        self.serialConnectButton.setText(_translate("AdcpTerminal", "Connect"))
        self.sendButton.setText(_translate("AdcpTerminal", "SEND"))
        self.breakButton.setText(_translate("AdcpTerminal", "BREAK"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AdcpTerminal = QtWidgets.QMainWindow()
    ui = Ui_AdcpTerminal()
    ui.setupUi(AdcpTerminal)
    AdcpTerminal.show()
    sys.exit(app.exec_())

