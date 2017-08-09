import json
import os
import sys
from subsystem_view import Ui_Subsystem
from PyQt5.QtWidgets import QWidget

import ADCP.Predictor.Power  as Power
import ADCP.Predictor.Range as Range
import ADCP.Predictor.MaxVelocity as Velocity
import ADCP.Predictor.STD as STD
import ADCP.Predictor.DataStorage as DS
import ADCP.Subsystem as SS

import ADCP.AdcpCommands as Commands
import AdcpJson as JSON
import datetime
import time


class SubsystemVM(Ui_Subsystem, QWidget):
    """
    Subsystem settings.
    """

    def __init__(self, parent, predictor, ss_code):
        Ui_Subsystem.__init__(self)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.predictor = predictor
        self.ss_code = ss_code
        self.freq = SS.ss_frequency(ss_code)

        # Set the label
        #self.freqLabel.setText("[" + str(ss_code) + "] - " + SS.ss_label(ss_code))

        # Set the style
        #self.freqLabel.setStyleSheet("font-weight: bold; color: red; font-size: 16px")
        self.pingingTextBrowser.setStyleSheet(
            "font-size: 8pt; background-color: transparent")
        self.errorTextBrowser.setStyleSheet(
            "font-size: 8pt; background-color: transparent")
        self.powerLabel.setStyleSheet("font-weight: bold; color: blue; font-size: 8pt")
        self.numBatteriesLabel.setStyleSheet("font-weight: bold; color: blue; font-size: 8pt")
        self.wpRangeLabel.setStyleSheet("font-weight: bold; color: blue; font-size: 10pt")
        self.btRangeLabel.setStyleSheet("font-weight: bold; color: blue; font-size: 10pt")
        self.firstBinPosLabel.setStyleSheet("font-weight: bold; color: blue; font-size: 10pt")
        self.maxVelLabel.setStyleSheet("font-weight: bold; color: blue; font-size: 10pt")
        self.dataUsageLabel.setStyleSheet("font-weight: bold; color: blue; font-size: 10pt")
        self.stdLabel.setStyleSheet("font-weight: bold; color: blue; font-size: 10pt")
        self.predictionGroupBox.setStyleSheet("QGroupBox#predictionGroupBox { background: #e3f2fd }\n QGroupBox::title { background-color: transparent; }")
        self.statusGroupBox.setStyleSheet("QGroupBox { background: #e0f2f1 }\n QGroupBox::title { background-color: transparent; }")
        self.errorGroupBox.setStyleSheet("QGroupBox { background: #ffebee }\n QGroupBox::title { background-color: transparent; }")

        # Set the values based off the preset
        self.presetButton.clicked.connect(self.set_preset)

        # Calculated results
        self.calc_power = 0.0
        self.calc_data = 0.0
        self.calc_num_batt = 0.0
        self.calc_max_vel = 0.0
        self.calc_std = 0.0
        self.calc_first_bin = 0.0
        self.calc_wp_range = 0.0
        self.calc_bt_range = 0.0
        self.calc_cfg_wp_range = 0.0

        # Initialize
        self.init_list()
        self.set_tooltips()

        # Get the checkbox state
        self.cwponCheckBox.stateChanged.connect(self.cwpon_enable_disable)
        self.cbtonCheckBox.stateChanged.connect(self.cbton_enable_disable)
        self.cbiEnabledCheckBox.stateChanged.connect(self.cbi_enable_disable)
        self.rangeTrackingComboBox.currentIndexChanged.connect(self.cwprt_enable_disable)

        # Init defaults
        self.cwponCheckBox.setCheckState(2)
        self.cbtonCheckBox.setCheckState(0)
        self.cbton_enable_disable(0)                    # Disable CBTON by default
        self.cbiEnabledCheckBox.setCheckState(0)
        self.cbi_enable_disable(0)                      # Disable CBI by default
        self.cedBeamVelCheckBox.setCheckState(2)
        self.cedInstrVelCheckBox.setCheckState(2)
        self.cedEarthVelCheckBox.setCheckState(2)
        self.cedAmpCheckBox.setCheckState(2)
        self.cedCorrCheckBox.setCheckState(2)
        self.cedBeamGoodPingCheckBox.setCheckState(2)
        self.cedEarthGoodPingCheckBox.setCheckState(2)
        self.cedEnsCheckBox.setCheckState(2)
        self.cedAncCheckBox.setCheckState(2)
        self.cedBtCheckBox.setCheckState(2)
        self.cedNmeaCheckBox.setCheckState(2)
        self.cedWpEngCheckBox.setCheckState(2)
        self.cedBtEngCheckBox.setCheckState(2)
        self.cedSysSettingCheckBox.setCheckState(2)
        self.cedRangeTrackingCheckBox.setCheckState(2)

        # Check SS code to know how many beams
        if self.ss_code == 'A' or self.ss_code == 'B' or self.ss_code == 'C' or self.ss_code == 'D' or self.ss_code == 'E':
            self.numBeamsSpinBox.setValue(1)

        # Watch for changes to recalculate
        self.cedBeamVelCheckBox.stateChanged.connect(self.stateChanged)
        self.cedInstrVelCheckBox.stateChanged.connect(self.stateChanged)
        self.cedEarthVelCheckBox.stateChanged.connect(self.stateChanged)
        self.cedAmpCheckBox.stateChanged.connect(self.stateChanged)
        self.cedCorrCheckBox.stateChanged.connect(self.stateChanged)
        self.cedBeamGoodPingCheckBox.stateChanged.connect(self.stateChanged)
        self.cedEarthGoodPingCheckBox.stateChanged.connect(self.stateChanged)
        self.cedEnsCheckBox.stateChanged.connect(self.stateChanged)
        self.cedAncCheckBox.stateChanged.connect(self.stateChanged)
        self.cedBtCheckBox.stateChanged.connect(self.stateChanged)
        self.cedNmeaCheckBox.stateChanged.connect(self.stateChanged)
        self.cedWpEngCheckBox.stateChanged.connect(self.stateChanged)
        self.cedBtEngCheckBox.stateChanged.connect(self.stateChanged)
        self.cedSysSettingCheckBox.stateChanged.connect(self.stateChanged)
        self.cedRangeTrackingCheckBox.stateChanged.connect(self.stateChanged)
        self.cwpblDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cwpbsDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cwpbnSpinBox.valueChanged.connect(self.valueChanged)
        self.cwpbbDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cwpbbComboBox.currentIndexChanged.connect(self.valueChanged)
        self.cwppSpinBox.valueChanged.connect(self.valueChanged)
        self.cwptbpDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cbtbbComboBox.currentIndexChanged.connect(self.valueChanged)
        self.cbttbpDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cbiBurstIntervalDoubleSpinBox.valueChanged.connect(self.valueChanged)
        self.cbiNumEnsSpinBox.valueChanged.connect(self.valueChanged)
        self.cbiInterleaveCheckBox.stateChanged.connect(self.valueChanged)
        self.numBeamsSpinBox.valueChanged.connect(self.valueChanged)
        self.cwprtRangeFractionSpinBox.valueChanged.connect(self.valueChanged)
        self.cwprtMinBinSpinBox.valueChanged.connect(self.valueChanged)
        self.cwprtMaxBinSpinBox.valueChanged.connect(self.valueChanged)

        # Show initial results
        self.calculate()

    def init_list(self):
        self.cwpbbComboBox.addItem("Broadband", 1)
        self.cwpbbComboBox.addItem("Narrowband", 0)

        self.cbtbbComboBox.addItem("Broadband", 1)
        self.cbtbbComboBox.addItem("Narrowband", 0)

        self.recommendCfgComboBox.addItem("Default", "Default")
        self.recommendCfgComboBox.addItem("Seafloor Mount", "Seafloor Mount")
        self.recommendCfgComboBox.addItem("Moving Boat", "Moving Boat")
        self.recommendCfgComboBox.addItem("General Purpose [WM1]", "WM1")
        self.recommendCfgComboBox.addItem("Shallow Slow-Moving [WM5]", "WM5")
        self.recommendCfgComboBox.addItem("Shallow [WM8]", "WM8")
        self.recommendCfgComboBox.addItem("Waves", "Waves")
        self.recommendCfgComboBox.addItem("DVL", "DVL")

        self.rangeTrackingComboBox.addItem("Disable", 0)
        self.rangeTrackingComboBox.addItem("Bin", 1)
        self.rangeTrackingComboBox.addItem("Pressure", 2)
        self.cwprtRangeFractionSpinBox.setEnabled(0)
        self.cwprtMinBinSpinBox.setEnabled(0)
        self.cwprtMaxBinSpinBox.setEnabled(0)

    def closeTab(self):
        """
        Close this tab.
        :return:
        """
        self.predictor.tab_close_requested(self.index)

    def set_tooltips(self):
        """
        Set the tooltip for all the values.  The tooltip will be found
        in a JSON file.  This file can be changed for other languages.
        :return:
        """
        # Get the JSON file
        cmds = JSON.get_json()
        if cmds is None:
            return

        # Set the tooltip
        self.cwponCheckBox.setToolTip(Commands.get_tooltip(cmds["CWPON"]["desc"]))
        self.cwpblDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBL"]["desc"]))
        self.cwpbsDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBS"]["desc"]))
        self.cwpbnSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBN"]["desc"]))
        self.cwpbbDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBB"]["desc"]))
        self.cwpbbComboBox.setToolTip(Commands.get_tooltip(cmds["CWPBB"]["desc"]))
        self.cwppSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPP"]["desc"]))
        self.cwptbpDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPTBP"]["desc"]))
        self.cbtonCheckBox.setToolTip(Commands.get_tooltip(cmds["CBTON"]["desc"]))
        self.cbtbbComboBox.setToolTip(Commands.get_tooltip(cmds["CBTBB"]["desc"]))
        self.cbttbpDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CBTTBP"]["desc"]))
        self.rangeTrackingComboBox.setToolTip(Commands.get_tooltip(cmds["CWPRT"]["desc"]))
        self.cwprtRangeFractionSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPRT"]["desc"]))
        self.cwprtMinBinSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPRT"]["desc"]))
        self.cwprtMaxBinSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPRT"]["desc"]))
        self.cbiEnabledCheckBox.setToolTip(Commands.get_tooltip(cmds["CBI"]["desc"]))
        self.cbiBurstIntervalDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CBI"]["desc"]))
        self.cbiInterleaveCheckBox.setToolTip(Commands.get_tooltip(cmds["CBI"]["desc"]))
        self.cbiNumEnsSpinBox.setToolTip(Commands.get_tooltip(cmds["CBI"]["desc"]))
        self.cedGroupBox.setToolTip(Commands.get_tooltip(cmds["CED"]["desc"]))
        self.predictionGroupBox.setToolTip("Prediction results for the subsystem configuration.")
        self.statusGroupBox.setToolTip("Status of the configuration based off the settings.")
        self.errorGroupBox.setToolTip("Any errors based off the configuration.")
        self.numBeamsGroupBox.setToolTip("Number of beams for the subsystem configuration.\nVertical beam configuration will be 1 beam.")
        self.recommendSettingGroupBox.setToolTip("Select a recommend settings for your deployment.\nThis will load a default setup to begin the configuration.")


    def stateChanged(self, state):
        """
        Monitor for any state changes then recalculate.
        :param state:
        :return:
        """
        # Recalculate
        self.predictor.calculate()

    def valueChanged(self, value):
        """
        Monitor for any value changes then recalculate.
        :param state:
        :return:
        """
        # Recalculate
        self.predictor.calculate()

    def cwpon_enable_disable(self, state):
        """
        Change the enable state of the values based off
        the selection of CWPON.
        :param state:
        :return:
        """
        enable_state = True
        if state == 2:
            enable_state = True
        else:
            enable_state = False

        self.cwpblDoubleSpinBox.setEnabled(enable_state)
        self.cwpbsDoubleSpinBox.setEnabled(enable_state)
        self.cwpbnSpinBox.setEnabled(enable_state)
        self.cwpbbDoubleSpinBox.setEnabled(enable_state)
        self.cwpbbComboBox.setEnabled(enable_state)
        self.cwppSpinBox.setEnabled(enable_state)
        self.cwptbpDoubleSpinBox.setEnabled(enable_state)

        # Recalculate
        self.predictor.calculate()

    def cbton_enable_disable(self, state):
        """
        Change the enable state of the values based off
        the selection of CBTON.
        :param state:
        :return:
        """
        enable_state = True
        if state == 2:
            enable_state = True
        else:
            enable_state = False

        self.cbtbbComboBox.setEnabled(enable_state)
        self.cbttbpDoubleSpinBox.setEnabled(enable_state)

        # Recalculate
        self.predictor.calculate()

    def cbi_enable_disable(self, state):
        """
        Change the enable state of the values based off
        the selection of Burst Mode.
        :param state:
        :return:
        """
        enable_state = True
        if state == 2:
            enable_state = True
        else:
            enable_state = False

        self.cbiBurstIntervalDoubleSpinBox.setEnabled(enable_state)
        self.cbiNumEnsSpinBox.setEnabled(enable_state)

        # Recalculate
        self.predictor.calculate()

    def cwprt_enable_disable(self, index):
        """
        Change the enable state of the values based off
        the selection of CWPRT.
        :param index: Current index.
        :return:
        """

        if index == 1:                                                                  # Bin
            self.cwprtRangeFractionSpinBox.setEnabled(0)
            self.cwprtMinBinSpinBox.setEnabled(1)
            self.cwprtMaxBinSpinBox.setEnabled(1)
            if self.cwprtMaxBinSpinBox.value() == 0:                                    # Set a default value
                self.cwprtMaxBinSpinBox.setValue(self.cwpbnSpinBox.value()-1)
        elif index == 2:                                                                # Pressure
            self.cwprtRangeFractionSpinBox.setEnabled(1)
            self.cwprtMinBinSpinBox.setEnabled(0)
            self.cwprtMaxBinSpinBox.setEnabled(0)
        else:                                                                           # Disabled
            self.cwprtRangeFractionSpinBox.setEnabled(0)
            self.cwprtMinBinSpinBox.setEnabled(0)
            self.cwprtMaxBinSpinBox.setEnabled(0)

        # Recalculate
        self.predictor.calculate()

    def calculate(self):
        """
        Calculate the prediction model results based off the settings.
        :return:
        """
        # Get the global settings
        deployment = self.predictor.deploymentDurationSpinBox.value()
        cei = self.predictor.ceiDoubleSpinBox.value()

        # Calculate
        self.calc_power = Power.calculate_power(DeploymentDuration=deployment,
                                                Beams=self.numBeamsSpinBox.value(),
                                                CEI=cei,
                                                SystemFrequency=self.freq,
                                                CWPON=self.cwponCheckBox.isChecked(),
                                                CWPBL=self.cwpblDoubleSpinBox.value(),
                                                CWPBS=self.cwpbsDoubleSpinBox.value(),
                                                CWPBN=self.cwpbnSpinBox.value(),
                                                CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()),
                                                CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                                CWPP=self.cwppSpinBox.value(),
                                                CWPTBP=self.cwptbpDoubleSpinBox.value(),
                                                CBTON=self.cbtonCheckBox.isChecked(),
                                                CBTBB=self.cbtbbComboBox.itemData(self.cbtbbComboBox.currentIndex()),)

        if self.cbiEnabledCheckBox.isChecked():
            self.calc_power = Power.calculate_burst_power(DeploymentDuration=deployment,
                                                          Beams=self.numBeamsSpinBox.value(),
                                                          CEI=cei,
                                                          SystemFrequency=self.freq,
                                                          CWPON=self.cwponCheckBox.isChecked(),
                                                          CWPBL=self.cwpblDoubleSpinBox.value(),
                                                          CWPBS=self.cwpbsDoubleSpinBox.value(),
                                                          CWPBN=self.cwpbnSpinBox.value(),
                                                          CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()),
                                                          CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                                          CWPP=self.cwppSpinBox.value(),
                                                          CWPTBP=self.cwptbpDoubleSpinBox.value(),
                                                          CBTON=self.cbtonCheckBox.isChecked(),
                                                          CBTBB=self.cbtbbComboBox.itemData(self.cbtbbComboBox.currentIndex()),
                                                          CBI=self.cbiEnabledCheckBox.isChecked(),
                                                          CBI_BurstInterval=self.cbiBurstIntervalDoubleSpinBox.value(),
                                                          CBI_NumEns=self.cbiNumEnsSpinBox.value(),)


        self.calc_num_batt = Power.calculate_number_batteries(DeploymentDuration=deployment, PowerUsage=self.calc_power)



        (bt_range, wp_range, first_bin, cfg_range) = Range.calculate_predicted_range(SystemFrequency=self.freq,
                                                Beams=self.numBeamsSpinBox.value(),
                                                CWPON=self.cwponCheckBox.isChecked(),
                                                CWPBL=self.cwpblDoubleSpinBox.value(),
                                                CWPBS=self.cwpbsDoubleSpinBox.value(),
                                                CWPBN=self.cwpbnSpinBox.value(),
                                                CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()),
                                                CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                                CWPP=self.cwppSpinBox.value(),
                                                CWPTBP=self.cwptbpDoubleSpinBox.value(),
                                                CBTON=self.cbtonCheckBox.isChecked())

        self.calc_bt_range = bt_range
        self.calc_wp_range = wp_range
        self.calc_first_bin = first_bin
        self.calc_cfg_wp_range = cfg_range

        self.calc_max_vel = Velocity.calculate_max_velocity(SystemFrequency=self.freq,
                                                            Beams=self.numBeamsSpinBox.value(),
                                                            CWPON=self.cwponCheckBox.isChecked(),
                                                            CWPBL=self.cwpblDoubleSpinBox.value(),
                                                            CWPBS=self.cwpbsDoubleSpinBox.value(),
                                                            CWPBN=self.cwpbnSpinBox.value(),
                                                            CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()),
                                                            CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                                            CWPP=self.cwppSpinBox.value(),
                                                            CWPTBP=self.cwptbpDoubleSpinBox.value(),
                                                            CBTON=self.cbtonCheckBox.isChecked())

        if self.cbiEnabledCheckBox.isChecked():
            self.calc_data = DS.calculate_burst_storage_amount(CBI_BurstInterval=self.cbiBurstIntervalDoubleSpinBox.value(),
                                                               CBI_NumEns=self.cbiNumEnsSpinBox.value(),
                                                               DeploymentDuration=deployment,
                                                               Beams=self.numBeamsSpinBox.value(),
                                                               CEI=cei,
                                                               CWPBN=self.cwpbnSpinBox.value(),
                                                               IsE0000001=self.cedBeamVelCheckBox.isChecked(),
                                                               IsE0000002=self.cedInstrVelCheckBox.isChecked(),
                                                               IsE0000003=self.cedEarthVelCheckBox.isChecked(),
                                                               IsE0000004=self.cedAmpCheckBox.isChecked(),
                                                               IsE0000005=self.cedCorrCheckBox.isChecked(),
                                                               IsE0000006=self.cedBeamGoodPingCheckBox.isChecked(),
                                                               IsE0000007=self.cedEarthGoodPingCheckBox.isChecked(),
                                                               IsE0000008=self.cedEnsCheckBox.isChecked(),
                                                               IsE0000009=self.cedAncCheckBox.isChecked(),
                                                               IsE0000010=self.cedBtCheckBox.isChecked(),
                                                               IsE0000011=self.cedNmeaCheckBox.isChecked(),
                                                               IsE0000012=self.cedWpEngCheckBox.isChecked(),
                                                               IsE0000013=self.cedBtEngCheckBox.isChecked(),
                                                               IsE0000014=self.cedSysSettingCheckBox.isChecked(),
                                                               IsE0000015=self.cedRangeTrackingCheckBox.isChecked(),)
        else:
            self.calc_data = DS.calculate_storage_amount(DeploymentDuration=deployment,
                                                         CEI=cei,
                                                         Beams=self.numBeamsSpinBox.value(),
                                                         CWPBN=self.cwpbnSpinBox.value(),
                                                         IsE0000001=self.cedBeamVelCheckBox.isChecked(),
                                                         IsE0000002=self.cedInstrVelCheckBox.isChecked(),
                                                         IsE0000003=self.cedEarthVelCheckBox.isChecked(),
                                                         IsE0000004=self.cedAmpCheckBox.isChecked(),
                                                         IsE0000005=self.cedCorrCheckBox.isChecked(),
                                                         IsE0000006=self.cedBeamGoodPingCheckBox.isChecked(),
                                                         IsE0000007=self.cedEarthGoodPingCheckBox.isChecked(),
                                                         IsE0000008=self.cedEnsCheckBox.isChecked(),
                                                         IsE0000009=self.cedAncCheckBox.isChecked(),
                                                         IsE0000010=self.cedBtCheckBox.isChecked(),
                                                         IsE0000011=self.cedNmeaCheckBox.isChecked(),
                                                         IsE0000012=self.cedWpEngCheckBox.isChecked(),
                                                         IsE0000013=self.cedBtEngCheckBox.isChecked(),
                                                         IsE0000014=self.cedSysSettingCheckBox.isChecked(),
                                                         IsE0000015=self.cedRangeTrackingCheckBox.isChecked(),)


        self.calc_std = STD.calculate_std(SystemFrequency=self.freq,
                                          Beams=self.numBeamsSpinBox.value(),
                                          CWPON=self.cwponCheckBox.isChecked(),
                                          CWPBL=self.cwpblDoubleSpinBox.value(),
                                          CWPBS=self.cwpbsDoubleSpinBox.value(),
                                          CWPBN=self.cwpbnSpinBox.value(),
                                          CWPBB=self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex()),
                                          CWPBB_LagLength=self.cwpbbDoubleSpinBox.value(),
                                          CWPP=self.cwppSpinBox.value(),
                                          CWPTBP=self.cwptbpDoubleSpinBox.value(),
                                          CBTON=self.cbtonCheckBox.isChecked())

        # Update the display
        self.powerLabel.setText(str(round(self.calc_power, 3)) + " watt/hr")
        self.numBatteriesLabel.setText(str(round(self.calc_num_batt, 3)) + " batteries")
        self.wpRangeLabel.setText(str(round(self.calc_wp_range, 3)) + " m")
        self.btRangeLabel.setText(str(round(self.calc_bt_range, 3)) + " m")
        self.firstBinPosLabel.setText(str(round(self.calc_first_bin, 3)) + " m")
        self.maxVelLabel.setText(str(round(self.calc_max_vel, 3)) + " m/s")
        self.dataUsageLabel.setText(str(DS.bytes_2_human_readable(self.calc_data)))
        self.stdLabel.setText(str(round(self.calc_std, 3)) + " m/s")


        # Set the ping description
        self.pingingTextBrowser.clear()
        cfg_status_str = ""
        err_status_str = ""

        # CBI
        if self.cbiEnabledCheckBox.isChecked():
            msg, error_msg = Commands.pretty_print_burst(self.predictor.ceiDoubleSpinBox.value(),
                                                          self.cbiBurstIntervalDoubleSpinBox.value(),
                                                          self.cbiNumEnsSpinBox.value(),
                                                          self.cwppSpinBox.value(),
                                                          self.cwptbpDoubleSpinBox.value())
            cfg_status_str += msg
            err_status_str += error_msg
        else:
            msg, error_msg = Commands.pretty_print_standard(self.predictor.ceiDoubleSpinBox.value(),
                                           self.cwppSpinBox.value(),
                                           self.cwptbpDoubleSpinBox.value())
            cfg_status_str += msg
            err_status_str += error_msg

        if self.cwponCheckBox.isChecked():
            # Configured Water Profile depth
            msg = Commands.pretty_print_cfg_depth(self.cwpblDoubleSpinBox.value(),
                                                                         self.cwpbsDoubleSpinBox.value(),
                                                                         self.cwpbnSpinBox.value(),
                                                                         self.calc_first_bin)
            cfg_status_str += msg
            err_status_str += error_msg

        # Max Velocity and Accuracy tooltip
        max_vel_acc_tt, error_msg = Commands.pretty_print_accuracy(self.calc_max_vel, self.calc_std)
        err_status_str += error_msg
        self.velAccGroupBox.setToolTip(max_vel_acc_tt)
        self.maxVelLabel.setToolTip(max_vel_acc_tt)
        self.stdLabel.setToolTip(max_vel_acc_tt)
        if self.cwponCheckBox.isChecked():
            cfg_status_str += max_vel_acc_tt

        # Recording turned on
        if self.predictor.cerecordCheckBox.isChecked():
            cfg_status_str += "-Recording to the internal SD card.\n"

        # Set the text to the browser
        self.pingingTextBrowser.setText(cfg_status_str)
        self.errorTextBrowser.setText(err_status_str)

    def get_cmd_list(self):
        """
        Create a list of commands.
        :return: List of all the commands with the values.
        """
        command_list = []

        if self.cwponCheckBox.isChecked():
            # CWPON
            if self.cwponCheckBox.isChecked():
                command_list.append(Commands.AdcpCmd("CWPON", "1"))
            else:
                command_list.append(Commands.AdcpCmd("CWPON", "0"))

            # CWPBB
            cwpbb_val = self.cwpbbComboBox.itemData(self.cwpbbComboBox.currentIndex())
            cwpbb_lag = str(self.cwpbbDoubleSpinBox.value())
            command_list.append((Commands.AdcpCmd("CWPBB", str(cwpbb_val) + ", " + cwpbb_lag)))

            command_list.append(Commands.AdcpCmd("CWPBL", str(self.cwpblDoubleSpinBox.value())))        # CWPBL
            command_list.append(Commands.AdcpCmd("CWPBS", str(self.cwpbsDoubleSpinBox.value())))        # CWPBS
            command_list.append(Commands.AdcpCmd("CWPBN", str(self.cwpbnSpinBox.value())))              # CWPBS
            command_list.append(Commands.AdcpCmd("CWPP", str(self.cwppSpinBox.value())))                # CWPP
            command_list.append(Commands.AdcpCmd("CWPTBP", str(self.cwptbpDoubleSpinBox.value())))      # CWPTBP

            # CWPRT
            if self.rangeTrackingComboBox.currentIndex() == 0:
                command_list.append(Commands.AdcpCmd("CWPRT", str(0)))                                  # CWPRT
            elif self.rangeTrackingComboBox.currentIndex() == 1:
                minBin = str(self.cwprtMinBinSpinBox.value())
                maxBin = str(self.cwprtMaxBinSpinBox.value())
                command_list.append(Commands.AdcpCmd("CWPRT", "1, " + minBin + ", " + maxBin))          # CWPRT
            elif self.rangeTrackingComboBox.currentIndex() == 2:
                frac = str(self.cwprtRangeFractionSpinBox.value())
                command_list.append(Commands.AdcpCmd("CWPRT", "2, " + frac))                            # CWPRT

        if self.cbtonCheckBox.isChecked():
            # CBTON
            if self.cbtonCheckBox.isChecked():
                command_list.append(Commands.AdcpCmd("CBTON", "1"))
            else:
                command_list.append(Commands.AdcpCmd("CBTON", "0"))

            #CBTBB
            cbtbb_val = self.cbtbbComboBox.itemData(self.cbtbbComboBox.currentIndex())
            if cbtbb_val == 0:
                command_list.append((Commands.AdcpCmd("CBTBB", "0")))
            else:
                command_list.append((Commands.AdcpCmd("CBTBB", "7")))

            command_list.append(Commands.AdcpCmd("CBTTBP", str(self.cbttbpDoubleSpinBox.value())))      # CBTTBP

        if self.cbiEnabledCheckBox.isChecked():
            cbi_num_ens = str(self.cbiNumEnsSpinBox.value())
            cbi_interval = Commands.sec_to_hmss(self.cbiBurstIntervalDoubleSpinBox.value())
            if self.cbiInterleaveCheckBox.isChecked():
                command_list.append(Commands.AdcpCmd("CBI", cbi_interval + ", " + cbi_num_ens + " ,1"))     # CBI
            else:
                command_list.append(Commands.AdcpCmd("CBI", cbi_interval + ", " + cbi_num_ens + " ,0"))     # CBI

        # CED
        ced = ""
        if self.cedBeamVelCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedInstrVelCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedEarthVelCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedAmpCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedCorrCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedBeamGoodPingCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedEarthGoodPingCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedEnsCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedAncCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedBtCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedNmeaCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedWpEngCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedBtEngCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedSysSettingCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        if self.cedRangeTrackingCheckBox.isChecked():
            ced += "1"
        else:
            ced += "0"

        ced += "00000000000000000"
        command_list.append(Commands.AdcpCmd("CED", ced))               # CED


        return command_list

    def set_preset(self):
        """
        Set the presets from the JSON file.
        :return:
        """
        # Get the JSON file
        json_cmds = JSON.get_json()
        if json_cmds is None:
            return

        if self.recommendCfgComboBox.currentText() == "Default":                                   # Default
            print("Default")
            if self.ss_code == "2":                                                         # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
            elif self.ss_code == "3":                                                         # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
            elif self.ss_code == "4":                                                         # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Default"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)

        elif self.recommendCfgComboBox.currentText() == "General Purpose [WM1]":                                     # WM1
            print("WM1")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM1"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)

        elif self.recommendCfgComboBox.currentText() == "Shallow Slow-Moving [WM5]":  # WM5 and Shallow Slow-Moving
            print("WM5")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM5"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)

        elif self.recommendCfgComboBox.currentText() == "Shallow [WM8]":  # WM8 and Shallow
            print("WM8")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(True)
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(True)
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["WM8"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(False)

        elif self.recommendCfgComboBox.currentText() == "Seafloor Mount":  # Bottom Mount
            print("Seafloor Mount")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["1200"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["1200"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["1200"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Seafloor"]["1200"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["1200"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["600"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["600"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["600"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Seafloor"]["600"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["600"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["300"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["300"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Seafloor"]["300"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Seafloor"]["300"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Seafloor"]["300"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)

        elif self.recommendCfgComboBox.currentText() == "Waves":  # Waves
            print("Waves")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Waves"]["1200"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Waves"]["1200"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Waves"]["1200"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Waves"]["1200"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Waves"]["1200"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Waves"]["600"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Waves"]["600"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Waves"]["600"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Waves"]["600"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Waves"]["600"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["Waves"]["300"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["Waves"]["300"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["Waves"]["300"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["Waves"]["300"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["Waves"]["300"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(True)

        elif self.recommendCfgComboBox.currentText() == "Moving Boat":  # Moving Boat
            print("Moving Boat")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["1200"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["1200"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["1200"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["600"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["600"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["600"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["MovingBoat"]["600"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["600"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["300"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["300"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["MovingBoat"]["300"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["MovingBoat"]["300"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["MovingBoat"]["300"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)

        elif self.recommendCfgComboBox.currentText() == "DVL":  # DVL
            print("DVL")
            if self.ss_code == "2":  # 1200 khz
                print("1200kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["DVL"]["1200"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["DVL"]["1200"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["DVL"]["1200"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["DVL"]["1200"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["DVL"]["1200"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
            elif self.ss_code == "3":  # 600 khz
                print("600kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["DVL"]["600"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["DVL"]["600"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["DVL"]["600"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["DVL"]["600"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["DVL"]["600"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)
            elif self.ss_code == "4":  # 300 khz
                print("300kHz")
                self.cwponCheckBox.setChecked(json_cmds["Setups"]["DVL"]["300"]["CWPON"])
                self.cwpblDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPBL"])
                self.cwpbsDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPBS"])
                self.cwpbnSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPBN"])
                self.cwpbbComboBox.setCurrentIndex(0)
                self.cwpbbDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPBB_Lag"])
                self.cwppSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPP"])
                self.cwptbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPTBP"])
                self.cbtonCheckBox.setChecked(json_cmds["Setups"]["DVL"]["300"]["CBTON"])
                self.cbtbbComboBox.setCurrentIndex(0)
                self.cbttbpDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CBTTBP"])
                self.cbiEnabledCheckBox.setChecked(json_cmds["Setups"]["DVL"]["300"]["CBI_Enabled"])
                self.cbiBurstIntervalDoubleSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CBI_BusrtInterval"])
                self.cbiNumEnsSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CBI_NumEns"])
                self.rangeTrackingComboBox.setCurrentIndex(json_cmds["Setups"]["DVL"]["300"]["CWPRT_Mode"])
                self.cwprtMinBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPRT_MinBin"])
                self.cwprtMaxBinSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPRT_MaxBin"])
                self.cwprtRangeFractionSpinBox.setValue(json_cmds["Setups"]["DVL"]["300"]["CWPRT_Pressure"])
                self.predictor.cerecordCheckBox.setChecked(False)

