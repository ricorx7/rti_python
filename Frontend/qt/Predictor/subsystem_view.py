# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'subsystem_view.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Subsystem(object):
    def setupUi(self, Subsystem):
        Subsystem.setObjectName("Subsystem")
        Subsystem.resize(709, 826)
        self.groupBox_2 = QtWidgets.QGroupBox(Subsystem)
        self.groupBox_2.setGeometry(QtCore.QRect(330, 80, 311, 131))
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.groupBox_2)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(10, 30, 271, 91))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_9 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.cbtonCheckBox = QtWidgets.QCheckBox(self.formLayoutWidget_2)
        self.cbtonCheckBox.setText("")
        self.cbtonCheckBox.setObjectName("cbtonCheckBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbtonCheckBox)
        self.label_10 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.cbtbbComboBox = QtWidgets.QComboBox(self.formLayoutWidget_2)
        self.cbtbbComboBox.setObjectName("cbtbbComboBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cbtbbComboBox)
        self.label_11 = QtWidgets.QLabel(self.formLayoutWidget_2)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.cbttbpDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget_2)
        self.cbttbpDoubleSpinBox.setObjectName("cbttbpDoubleSpinBox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cbttbpDoubleSpinBox)
        self.groupBox_3 = QtWidgets.QGroupBox(Subsystem)
        self.groupBox_3.setGeometry(QtCore.QRect(330, 210, 311, 151))
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayoutWidget_3 = QtWidgets.QWidget(self.groupBox_3)
        self.formLayoutWidget_3.setGeometry(QtCore.QRect(10, 30, 281, 112))
        self.formLayoutWidget_3.setObjectName("formLayoutWidget_3")
        self.formLayout_3 = QtWidgets.QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_12 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_12.setObjectName("label_12")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.cbiEnabledCheckBox = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.cbiEnabledCheckBox.setText("")
        self.cbiEnabledCheckBox.setObjectName("cbiEnabledCheckBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbiEnabledCheckBox)
        self.label_13 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_13.setObjectName("label_13")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.cbiBurstIntervalDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget_3)
        self.cbiBurstIntervalDoubleSpinBox.setMinimum(0.0)
        self.cbiBurstIntervalDoubleSpinBox.setMaximum(86400.0)
        self.cbiBurstIntervalDoubleSpinBox.setProperty("value", 3600.0)
        self.cbiBurstIntervalDoubleSpinBox.setObjectName("cbiBurstIntervalDoubleSpinBox")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cbiBurstIntervalDoubleSpinBox)
        self.label_14 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_14.setObjectName("label_14")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.cbiNumEnsSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget_3)
        self.cbiNumEnsSpinBox.setMaximum(5000)
        self.cbiNumEnsSpinBox.setSingleStep(128)
        self.cbiNumEnsSpinBox.setProperty("value", 1024)
        self.cbiNumEnsSpinBox.setObjectName("cbiNumEnsSpinBox")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cbiNumEnsSpinBox)
        self.label_18 = QtWidgets.QLabel(self.formLayoutWidget_3)
        self.label_18.setObjectName("label_18")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_18)
        self.cbiInterleaveCheckBox = QtWidgets.QCheckBox(self.formLayoutWidget_3)
        self.cbiInterleaveCheckBox.setText("")
        self.cbiInterleaveCheckBox.setObjectName("cbiInterleaveCheckBox")
        self.formLayout_3.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cbiInterleaveCheckBox)
        self.groupBox = QtWidgets.QGroupBox(Subsystem)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 311, 251))
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 20, 261, 252))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.cwponCheckBox = QtWidgets.QCheckBox(self.formLayoutWidget)
        self.cwponCheckBox.setText("")
        self.cwponCheckBox.setObjectName("cwponCheckBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cwponCheckBox)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.cwpblDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.cwpblDoubleSpinBox.setSingleStep(0.25)
        self.cwpblDoubleSpinBox.setProperty("value", 0.5)
        self.cwpblDoubleSpinBox.setObjectName("cwpblDoubleSpinBox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cwpblDoubleSpinBox)
        self.label_3 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.cwpbsDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.cwpbsDoubleSpinBox.setMinimum(0.01)
        self.cwpbsDoubleSpinBox.setMaximum(200.0)
        self.cwpbsDoubleSpinBox.setSingleStep(0.1)
        self.cwpbsDoubleSpinBox.setProperty("value", 1.0)
        self.cwpbsDoubleSpinBox.setObjectName("cwpbsDoubleSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cwpbsDoubleSpinBox)
        self.label_4 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.cwpbnSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.cwpbnSpinBox.setMinimum(1)
        self.cwpbnSpinBox.setMaximum(200)
        self.cwpbnSpinBox.setProperty("value", 30)
        self.cwpbnSpinBox.setObjectName("cwpbnSpinBox")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cwpbnSpinBox)
        self.label_5 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.cwpbbDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.cwpbbDoubleSpinBox.setDecimals(3)
        self.cwpbbDoubleSpinBox.setSingleStep(0.05)
        self.cwpbbDoubleSpinBox.setProperty("value", 0.5)
        self.cwpbbDoubleSpinBox.setObjectName("cwpbbDoubleSpinBox")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.cwpbbDoubleSpinBox)
        self.label_6 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.cwpbbComboBox = QtWidgets.QComboBox(self.formLayoutWidget)
        self.cwpbbComboBox.setObjectName("cwpbbComboBox")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.cwpbbComboBox)
        self.label_7 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.cwppSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.cwppSpinBox.setMaximum(500)
        self.cwppSpinBox.setProperty("value", 1)
        self.cwppSpinBox.setObjectName("cwppSpinBox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.cwppSpinBox)
        self.label_8 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.cwptbpDoubleSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget)
        self.cwptbpDoubleSpinBox.setSingleStep(0.1)
        self.cwptbpDoubleSpinBox.setProperty("value", 0.1)
        self.cwptbpDoubleSpinBox.setObjectName("cwptbpDoubleSpinBox")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.cwptbpDoubleSpinBox)
        self.cedGroupBox = QtWidgets.QGroupBox(Subsystem)
        self.cedGroupBox.setGeometry(QtCore.QRect(10, 420, 631, 111))
        self.cedGroupBox.setObjectName("cedGroupBox")
        self.cedBeamVelCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedBeamVelCheckBox.setGeometry(QtCore.QRect(10, 20, 86, 20))
        self.cedBeamVelCheckBox.setObjectName("cedBeamVelCheckBox")
        self.cedInstrVelCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedInstrVelCheckBox.setGeometry(QtCore.QRect(10, 40, 111, 20))
        self.cedInstrVelCheckBox.setObjectName("cedInstrVelCheckBox")
        self.cedEarthVelCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedEarthVelCheckBox.setGeometry(QtCore.QRect(10, 60, 86, 20))
        self.cedEarthVelCheckBox.setObjectName("cedEarthVelCheckBox")
        self.cedAmpCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedAmpCheckBox.setGeometry(QtCore.QRect(10, 80, 86, 20))
        self.cedAmpCheckBox.setObjectName("cedAmpCheckBox")
        self.cedCorrCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedCorrCheckBox.setGeometry(QtCore.QRect(140, 20, 111, 20))
        self.cedCorrCheckBox.setObjectName("cedCorrCheckBox")
        self.cedBeamGoodPingCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedBeamGoodPingCheckBox.setGeometry(QtCore.QRect(140, 40, 131, 20))
        self.cedBeamGoodPingCheckBox.setObjectName("cedBeamGoodPingCheckBox")
        self.cedEarthGoodPingCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedEarthGoodPingCheckBox.setGeometry(QtCore.QRect(140, 60, 131, 20))
        self.cedEarthGoodPingCheckBox.setObjectName("cedEarthGoodPingCheckBox")
        self.cedEnsCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedEnsCheckBox.setGeometry(QtCore.QRect(140, 80, 86, 20))
        self.cedEnsCheckBox.setObjectName("cedEnsCheckBox")
        self.cedAncCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedAncCheckBox.setGeometry(QtCore.QRect(300, 20, 86, 20))
        self.cedAncCheckBox.setObjectName("cedAncCheckBox")
        self.cedBtCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedBtCheckBox.setGeometry(QtCore.QRect(300, 40, 121, 20))
        self.cedBtCheckBox.setObjectName("cedBtCheckBox")
        self.cedNmeaCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedNmeaCheckBox.setGeometry(QtCore.QRect(300, 60, 86, 20))
        self.cedNmeaCheckBox.setObjectName("cedNmeaCheckBox")
        self.cedWpEngCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedWpEngCheckBox.setGeometry(QtCore.QRect(300, 80, 131, 20))
        self.cedWpEngCheckBox.setObjectName("cedWpEngCheckBox")
        self.cedBtEngCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedBtEngCheckBox.setGeometry(QtCore.QRect(450, 20, 121, 20))
        self.cedBtEngCheckBox.setObjectName("cedBtEngCheckBox")
        self.cedSysSettingCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedSysSettingCheckBox.setGeometry(QtCore.QRect(450, 40, 131, 20))
        self.cedSysSettingCheckBox.setObjectName("cedSysSettingCheckBox")
        self.cedRangeTrackingCheckBox = QtWidgets.QCheckBox(self.cedGroupBox)
        self.cedRangeTrackingCheckBox.setGeometry(QtCore.QRect(450, 60, 131, 20))
        self.cedRangeTrackingCheckBox.setObjectName("cedRangeTrackingCheckBox")
        self.predictionGroupBox = QtWidgets.QGroupBox(Subsystem)
        self.predictionGroupBox.setGeometry(QtCore.QRect(10, 540, 631, 121))
        self.predictionGroupBox.setAutoFillBackground(False)
        self.predictionGroupBox.setObjectName("predictionGroupBox")
        self.rangeGroupBox = QtWidgets.QGroupBox(self.predictionGroupBox)
        self.rangeGroupBox.setGeometry(QtCore.QRect(220, 20, 201, 91))
        self.rangeGroupBox.setObjectName("rangeGroupBox")
        self.layoutWidget = QtWidgets.QWidget(self.rangeGroupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 181, 66))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_25 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_25.setFont(font)
        self.label_25.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_25.setObjectName("label_25")
        self.gridLayout_3.addWidget(self.label_25, 1, 0, 1, 1)
        self.label_27 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_27.setFont(font)
        self.label_27.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_27.setObjectName("label_27")
        self.gridLayout_3.addWidget(self.label_27, 2, 0, 1, 1)
        self.btRangeLabel = QtWidgets.QLabel(self.layoutWidget)
        self.btRangeLabel.setText("")
        self.btRangeLabel.setObjectName("btRangeLabel")
        self.gridLayout_3.addWidget(self.btRangeLabel, 2, 1, 1, 1)
        self.wpRangeLabel = QtWidgets.QLabel(self.layoutWidget)
        self.wpRangeLabel.setText("")
        self.wpRangeLabel.setObjectName("wpRangeLabel")
        self.gridLayout_3.addWidget(self.wpRangeLabel, 1, 1, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_23.setFont(font)
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.gridLayout_3.addWidget(self.label_23, 0, 0, 1, 1)
        self.firstBinPosLabel = QtWidgets.QLabel(self.layoutWidget)
        self.firstBinPosLabel.setText("")
        self.firstBinPosLabel.setObjectName("firstBinPosLabel")
        self.gridLayout_3.addWidget(self.firstBinPosLabel, 0, 1, 1, 1)
        self.powerDataGroupBox = QtWidgets.QGroupBox(self.predictionGroupBox)
        self.powerDataGroupBox.setGeometry(QtCore.QRect(10, 20, 201, 91))
        self.powerDataGroupBox.setObjectName("powerDataGroupBox")
        self.layoutWidget1 = QtWidgets.QWidget(self.powerDataGroupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 181, 68))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.dataUsageLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.dataUsageLabel.setText("")
        self.dataUsageLabel.setObjectName("dataUsageLabel")
        self.gridLayout_2.addWidget(self.dataUsageLabel, 2, 1, 1, 1)
        self.numBatteriesLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.numBatteriesLabel.setText("")
        self.numBatteriesLabel.setObjectName("numBatteriesLabel")
        self.gridLayout_2.addWidget(self.numBatteriesLabel, 1, 1, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName("label_17")
        self.gridLayout_2.addWidget(self.label_17, 1, 0, 1, 1)
        self.powerLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.powerLabel.setText("")
        self.powerLabel.setObjectName("powerLabel")
        self.gridLayout_2.addWidget(self.powerLabel, 0, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 0, 0, 1, 1)
        self.label_29 = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_29.setFont(font)
        self.label_29.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_29.setObjectName("label_29")
        self.gridLayout_2.addWidget(self.label_29, 2, 0, 1, 1)
        self.numBeamsGroupBox = QtWidgets.QGroupBox(Subsystem)
        self.numBeamsGroupBox.setGeometry(QtCore.QRect(330, 360, 311, 61))
        self.numBeamsGroupBox.setObjectName("numBeamsGroupBox")
        self.numBeamsSpinBox = QtWidgets.QSpinBox(self.numBeamsGroupBox)
        self.numBeamsSpinBox.setGeometry(QtCore.QRect(170, 30, 111, 24))
        self.numBeamsSpinBox.setMinimum(1)
        self.numBeamsSpinBox.setMaximum(4)
        self.numBeamsSpinBox.setProperty("value", 4)
        self.numBeamsSpinBox.setObjectName("numBeamsSpinBox")
        self.label_15 = QtWidgets.QLabel(self.numBeamsGroupBox)
        self.label_15.setGeometry(QtCore.QRect(48, 30, 111, 20))
        self.label_15.setObjectName("label_15")
        self.recommendSettingGroupBox = QtWidgets.QGroupBox(Subsystem)
        self.recommendSettingGroupBox.setGeometry(QtCore.QRect(330, 10, 311, 71))
        self.recommendSettingGroupBox.setObjectName("recommendSettingGroupBox")
        self.recommendCfgComboBox = QtWidgets.QComboBox(self.recommendSettingGroupBox)
        self.recommendCfgComboBox.setGeometry(QtCore.QRect(10, 30, 221, 26))
        self.recommendCfgComboBox.setObjectName("recommendCfgComboBox")
        self.presetButton = QtWidgets.QPushButton(self.recommendSettingGroupBox)
        self.presetButton.setGeometry(QtCore.QRect(240, 30, 61, 32))
        self.presetButton.setObjectName("presetButton")
        self.groupBox_11 = QtWidgets.QGroupBox(Subsystem)
        self.groupBox_11.setGeometry(QtCore.QRect(10, 260, 311, 161))
        self.groupBox_11.setObjectName("groupBox_11")
        self.formLayoutWidget_4 = QtWidgets.QWidget(self.groupBox_11)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(9, 30, 281, 124))
        self.formLayoutWidget_4.setObjectName("formLayoutWidget_4")
        self.formLayout_4 = QtWidgets.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_4.setContentsMargins(0, 0, 0, 0)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_20 = QtWidgets.QLabel(self.formLayoutWidget_4)
        self.label_20.setObjectName("label_20")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_20)
        self.rangeTrackingComboBox = QtWidgets.QComboBox(self.formLayoutWidget_4)
        self.rangeTrackingComboBox.setObjectName("rangeTrackingComboBox")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.rangeTrackingComboBox)
        self.label_22 = QtWidgets.QLabel(self.formLayoutWidget_4)
        self.label_22.setObjectName("label_22")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_22)
        self.cwprtRangeFractionSpinBox = QtWidgets.QDoubleSpinBox(self.formLayoutWidget_4)
        self.cwprtRangeFractionSpinBox.setProperty("value", 0.5)
        self.cwprtRangeFractionSpinBox.setObjectName("cwprtRangeFractionSpinBox")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cwprtRangeFractionSpinBox)
        self.label_24 = QtWidgets.QLabel(self.formLayoutWidget_4)
        self.label_24.setObjectName("label_24")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_24)
        self.cwprtMinBinSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget_4)
        self.cwprtMinBinSpinBox.setObjectName("cwprtMinBinSpinBox")
        self.formLayout_4.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cwprtMinBinSpinBox)
        self.label_26 = QtWidgets.QLabel(self.formLayoutWidget_4)
        self.label_26.setObjectName("label_26")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_26)
        self.cwprtMaxBinSpinBox = QtWidgets.QSpinBox(self.formLayoutWidget_4)
        self.cwprtMaxBinSpinBox.setObjectName("cwprtMaxBinSpinBox")
        self.formLayout_4.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.cwprtMaxBinSpinBox)
        self.velAccGroupBox = QtWidgets.QGroupBox(Subsystem)
        self.velAccGroupBox.setGeometry(QtCore.QRect(440, 560, 191, 91))
        self.velAccGroupBox.setObjectName("velAccGroupBox")
        self.layoutWidget2 = QtWidgets.QWidget(self.velAccGroupBox)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 30, 171, 51))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_19 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_19.setFont(font)
        self.label_19.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout.addWidget(self.label_19, 0, 0, 1, 1)
        self.maxVelLabel = QtWidgets.QLabel(self.layoutWidget2)
        self.maxVelLabel.setText("")
        self.maxVelLabel.setObjectName("maxVelLabel")
        self.gridLayout.addWidget(self.maxVelLabel, 0, 1, 1, 1)
        self.label_21 = QtWidgets.QLabel(self.layoutWidget2)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_21.setObjectName("label_21")
        self.gridLayout.addWidget(self.label_21, 1, 0, 1, 1)
        self.stdLabel = QtWidgets.QLabel(self.layoutWidget2)
        self.stdLabel.setText("")
        self.stdLabel.setObjectName("stdLabel")
        self.gridLayout.addWidget(self.stdLabel, 1, 1, 1, 1)
        self.statusGroupBox = QtWidgets.QGroupBox(Subsystem)
        self.statusGroupBox.setGeometry(QtCore.QRect(10, 670, 361, 121))
        self.statusGroupBox.setObjectName("statusGroupBox")
        self.pingingTextBrowser = QtWidgets.QTextBrowser(self.statusGroupBox)
        self.pingingTextBrowser.setGeometry(QtCore.QRect(10, 20, 341, 91))
        self.pingingTextBrowser.setObjectName("pingingTextBrowser")
        self.errorGroupBox = QtWidgets.QGroupBox(Subsystem)
        self.errorGroupBox.setGeometry(QtCore.QRect(380, 670, 261, 121))
        self.errorGroupBox.setObjectName("errorGroupBox")
        self.errorTextBrowser = QtWidgets.QTextBrowser(self.errorGroupBox)
        self.errorTextBrowser.setGeometry(QtCore.QRect(10, 20, 241, 91))
        self.errorTextBrowser.setObjectName("errorTextBrowser")

        self.retranslateUi(Subsystem)
        QtCore.QMetaObject.connectSlotsByName(Subsystem)

    def retranslateUi(self, Subsystem):
        _translate = QtCore.QCoreApplication.translate
        Subsystem.setWindowTitle(_translate("Subsystem", "MainWindow"))
        self.groupBox_2.setTitle(_translate("Subsystem", "Bottom Track"))
        self.label_9.setText(_translate("Subsystem", "CBTON"))
        self.label_10.setText(_translate("Subsystem", "CBTBB"))
        self.label_11.setText(_translate("Subsystem", "CBTTBP (s)"))
        self.groupBox_3.setTitle(_translate("Subsystem", "Burst Mode"))
        self.label_12.setText(_translate("Subsystem", "Burst Mode ON"))
        self.label_13.setText(_translate("Subsystem", "Burst Interval (s)"))
        self.label_14.setText(_translate("Subsystem", "Number of Ensembles"))
        self.label_18.setText(_translate("Subsystem", "Interleave"))
        self.groupBox.setTitle(_translate("Subsystem", "Water Profile"))
        self.label.setText(_translate("Subsystem", "CWPON"))
        self.label_2.setText(_translate("Subsystem", "CWPBL (m)"))
        self.label_3.setText(_translate("Subsystem", "CWPBS (m)"))
        self.label_4.setText(_translate("Subsystem", "CWPBN (bins)"))
        self.label_5.setText(_translate("Subsystem", "CWPBB Lag Length (m)"))
        self.label_6.setText(_translate("Subsystem", "Pulse Type"))
        self.label_7.setText(_translate("Subsystem", "CWPP (pings)"))
        self.label_8.setText(_translate("Subsystem", "CWPTBP (s)"))
        self.cedGroupBox.setTitle(_translate("Subsystem", "Data Output"))
        self.cedBeamVelCheckBox.setText(_translate("Subsystem", "Beam Vel"))
        self.cedInstrVelCheckBox.setText(_translate("Subsystem", "Instrument Vel"))
        self.cedEarthVelCheckBox.setText(_translate("Subsystem", "Earth Vel"))
        self.cedAmpCheckBox.setText(_translate("Subsystem", "Amplitude"))
        self.cedCorrCheckBox.setText(_translate("Subsystem", "Correlation"))
        self.cedBeamGoodPingCheckBox.setText(_translate("Subsystem", "Beam Good Ping"))
        self.cedEarthGoodPingCheckBox.setText(_translate("Subsystem", "Earth Good Ping"))
        self.cedEnsCheckBox.setText(_translate("Subsystem", "Ensemble"))
        self.cedAncCheckBox.setText(_translate("Subsystem", "Ancillary"))
        self.cedBtCheckBox.setText(_translate("Subsystem", "Bottom Track"))
        self.cedNmeaCheckBox.setText(_translate("Subsystem", "NMEA"))
        self.cedWpEngCheckBox.setText(_translate("Subsystem", "WP Engineering"))
        self.cedBtEngCheckBox.setText(_translate("Subsystem", "BT Engineering"))
        self.cedSysSettingCheckBox.setText(_translate("Subsystem", "System Settings"))
        self.cedRangeTrackingCheckBox.setText(_translate("Subsystem", "Range Tracking"))
        self.predictionGroupBox.setTitle(_translate("Subsystem", "Predictions"))
        self.rangeGroupBox.setTitle(_translate("Subsystem", "Maximum Range"))
        self.label_25.setText(_translate("Subsystem", "Water Profile Range: "))
        self.label_27.setText(_translate("Subsystem", "Bottom Track Range: "))
        self.label_23.setText(_translate("Subsystem", "First Bin Position: "))
        self.powerDataGroupBox.setTitle(_translate("Subsystem", "Power and Data"))
        self.label_17.setText(_translate("Subsystem", "Num Batteries: "))
        self.label_16.setText(_translate("Subsystem", "Power Usage: "))
        self.label_29.setText(_translate("Subsystem", "Data Usage: "))
        self.numBeamsGroupBox.setTitle(_translate("Subsystem", "Beams"))
        self.label_15.setText(_translate("Subsystem", "Number of Beams"))
        self.recommendSettingGroupBox.setTitle(_translate("Subsystem", "Recommend Setting"))
        self.presetButton.setText(_translate("Subsystem", "LOAD"))
        self.groupBox_11.setTitle(_translate("Subsystem", "Range Tracking"))
        self.label_20.setText(_translate("Subsystem", "Range Tracking"))
        self.label_22.setText(_translate("Subsystem", "Range Fraction"))
        self.label_24.setText(_translate("Subsystem", "Minimum Bin"))
        self.label_26.setText(_translate("Subsystem", "Maximum Bin"))
        self.velAccGroupBox.setTitle(_translate("Subsystem", "Velocity and Accuracy"))
        self.label_19.setText(_translate("Subsystem", "Maximum Velocity: "))
        self.label_21.setText(_translate("Subsystem", "Standard Deviation: "))
        self.statusGroupBox.setTitle(_translate("Subsystem", "Status"))
        self.errorGroupBox.setTitle(_translate("Subsystem", "Errors"))

