# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'predictor_view.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RoweTechPredictor(object):
    def setupUi(self, RoweTechPredictor):
        RoweTechPredictor.setObjectName("RoweTechPredictor")
        RoweTechPredictor.resize(1045, 818)
        self.centralWidget = QtWidgets.QWidget(RoweTechPredictor)
        self.centralWidget.setObjectName("centralWidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 40, 291, 141))
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 30, 271, 94))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.ceiDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.ceiDoubleSpinBox.setObjectName("ceiDoubleSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.ceiDoubleSpinBox)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.cwsSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.cwsSpinBox.setObjectName("cwsSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cwsSpinBox)
        self.deploymentDurationspinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.deploymentDurationspinBox.setObjectName("deploymentDurationspinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.deploymentDurationspinBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 190, 291, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.subsystemComboBox = QtWidgets.QComboBox(self.groupBox_2)
        self.subsystemComboBox.setGeometry(QtCore.QRect(10, 30, 271, 41))
        self.subsystemComboBox.setObjectName("subsystemComboBox")
        self.addSubsystemButton = QtWidgets.QPushButton(self.groupBox_2)
        self.addSubsystemButton.setGeometry(QtCore.QRect(150, 80, 113, 32))
        self.addSubsystemButton.setObjectName("addSubsystemButton")
        self.tabSubsystem = QtWidgets.QTabWidget(self.centralWidget)
        self.tabSubsystem.setEnabled(True)
        self.tabSubsystem.setGeometry(QtCore.QRect(320, 30, 671, 471))
        self.tabSubsystem.setObjectName("tabSubsystem")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabSubsystem.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabSubsystem.addTab(self.tab_4, "")
        RoweTechPredictor.setCentralWidget(self.centralWidget)

        self.retranslateUi(RoweTechPredictor)
        self.tabSubsystem.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(RoweTechPredictor)

    def retranslateUi(self, RoweTechPredictor):
        _translate = QtCore.QCoreApplication.translate
        RoweTechPredictor.setWindowTitle(_translate("RoweTechPredictor", "MainWindow"))
        self.groupBox.setTitle(_translate("RoweTechPredictor", "System Settings"))
        self.label.setText(_translate("RoweTechPredictor", "Deployment Duration (Days)"))
        self.label_2.setText(_translate("RoweTechPredictor", "CEI (s)"))
        self.label_3.setText(_translate("RoweTechPredictor", "CWS (ppt)"))
        self.groupBox_2.setTitle(_translate("RoweTechPredictor", "Subsystems"))
        self.addSubsystemButton.setText(_translate("RoweTechPredictor", "ADD"))
        self.tabSubsystem.setTabText(self.tabSubsystem.indexOf(self.tab_3), _translate("RoweTechPredictor", "Tab 1"))
        self.tabSubsystem.setTabText(self.tabSubsystem.indexOf(self.tab_4), _translate("RoweTechPredictor", "Tab 2"))

