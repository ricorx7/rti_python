import json
import os
from subsystem_view import Ui_Subsystem
from PyQt5.QtWidgets import QWidget

import ADCP.Predictor.Power  as Power
import ADCP.Predictor.Range as Range
import ADCP.Predictor.MaxVelocity as Velocity
import ADCP.Predictor.STD as STD
import ADCP.Predictor.DataStorage as DS
import ADCP.Subsystem as SS

import ADCP.AdcpCommands as Commands
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

        self.freqLabel.setText("[" + str(ss_code) + "] - " + SS.ss_label(ss_code))
        self.freqLabel.setStyleSheet("font-weight: bold; color: red; font-size: 16px")

        self.initList()
        self.set_tooltips()

        # Get the checkbox state
        self.cwponCheckBox.stateChanged.connect(self.cwpon_enable_disable)
        self.cbtonCheckBox.stateChanged.connect(self.cbton_enable_disable)
        self.cbiEnabledCheckBox.stateChanged.connect(self.cbi_enable_disable)

        # Init defaults
        self.cwponCheckBox.setCheckState(2)
        self.cbtonCheckBox.setCheckState(2)
        self.cbiEnabledCheckBox.setCheckState(0)
        self.cbi_enable_disable(0)
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
        self.numBeamsSpinBox.valueChanged.connect(self.valueChanged)

        # Show initial results
        self.calculate()

    def initList(self):
        self.cwpbbComboBox.addItem("Broadband", 1)
        self.cwpbbComboBox.addItem("Narrowband", 0)

        self.cbtbbComboBox.addItem("Broadband", 1)
        self.cbtbbComboBox.addItem("Narrowband", 0)

    def set_tooltips(self):
        # Get the configuration from the json file
        script_dir = os.path.dirname(__file__)
        # The path to this JSON file will not work if run from python script
        # But if built as an applicaiton with pyinstaller, this path will work
        json_file_path = os.path.join(script_dir, 'ADCP/AdcpCommands.json')
        try:
            cmds = json.loads(open(json_file_path).read())
        except Exception as e:
            print("Error opening predictor.JSON file", e)
            return

        self.cwpbbDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBB"]["desc"]))
        self.cwpbbComboBox.setToolTip(Commands.get_tooltip(cmds["CWPBB"]["desc"]))
        self.cwpbsDoubleSpinBox.setToolTip(Commands.get_tooltip(cmds["CWPBS"]["desc"]))


    #def get_tooltip(self, desc_array):
    #    return '\n'.join([str(x) for x in desc_array])

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

    def calculate(self):
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
        self.powerLabel.setText(str(round(self.calc_power, 4)) + " watts")
        self.powerLabel.setStyleSheet("font-weight: bold; color: blue")
        self.numBatteriesLabel.setText(str(round(self.calc_num_batt, 4)) + " batteries")
        self.numBatteriesLabel.setStyleSheet("font-weight: bold; color: blue")
        self.wpRangeLabel.setText(str(round(self.calc_wp_range, 4)) + " m")
        self.wpRangeLabel.setStyleSheet("font-weight: bold; color: blue")
        self.btRangeLabel.setText(str(round(self.calc_bt_range, 4)) + " m")
        self.btRangeLabel.setStyleSheet("font-weight: bold; color: blue")
        self.firstBinPosLabel.setText(str(round(self.calc_first_bin, 4)) + " m")
        self.firstBinPosLabel.setStyleSheet("font-weight: bold; color: blue")
        self.maxVelLabel.setText(str(round(self.calc_max_vel, 4)) + " m/s")
        self.maxVelLabel.setStyleSheet("font-weight: bold; color: blue")
        self.dataUsageLabel.setText(str(DS.bytes_2_human_readable(self.calc_data)))
        self.dataUsageLabel.setStyleSheet("font-weight: bold; color: blue")
        self.stdLabel.setText(str(round(self.calc_std, 4)) + " m/s")
        self.stdLabel.setStyleSheet("font-weight: bold; color: blue")

        self.pingingTextBrowser.clear()
        if self.cbiEnabledCheckBox.isChecked():
            self.pingingTextBrowser.setText(Commands.pretty_print_burst(self.predictor.ceiDoubleSpinBox.value(),
                                                                  self.cbiBurstIntervalDoubleSpinBox.value(),
                                                                  self.cbiNumEnsSpinBox.value(),
                                                                  self.cwppSpinBox.value(),
                                                                  self.cwptbpDoubleSpinBox.value()))
        else:
            self.pingingTextBrowser.setText(Commands.pretty_print_standard(self.predictor.ceiDoubleSpinBox.value(),
                                                                     self.cwppSpinBox.value(),
                                                                     self.cwptbpDoubleSpinBox.value()))
        self.pingingTextBrowser.setStyleSheet("font-weight: bold; color: blue; font-size: 10pt; background-color: transparent")

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
            command_list.append((Commands.AdcpCmd("CBTBB", str(cwpbb_val) + ", " + cwpbb_lag)))

            command_list.append(Commands.AdcpCmd("CWPBL", str(self.cwpblDoubleSpinBox.value())))        # CWPBL
            command_list.append(Commands.AdcpCmd("CWPBS", str(self.cwpbsDoubleSpinBox.value())))        # CWPBS
            command_list.append(Commands.AdcpCmd("CWPBN", str(self.cwpbnSpinBox.value())))              # CWPBS
            command_list.append(Commands.AdcpCmd("CWPP", str(self.cwppSpinBox.value())))                # CWPP
            command_list.append(Commands.AdcpCmd("CWPTBP", str(self.cwptbpDoubleSpinBox.value())))      # CWPTBP

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
            command_list.append(Commands.AdcpCmd("CBI", cbi_interval + ", " + cbi_num_ens + " ,0"))      # CBI

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


