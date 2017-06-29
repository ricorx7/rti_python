from subsystem_view import Ui_Subsystem
from PyQt5.QtWidgets import QWidget

class SubsystemVM(Ui_Subsystem, QWidget):
    """
    Subsystem settings.
    """

    def __init__(self, parent, predictor):
        Ui_Subsystem.__init__(self)
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.parent = parent
        self.predictor = predictor

        # Get the checkbox state
        self.cwponCheckBox.stateChanged.connect(self.cwpon_enable_disable)
        self.cbtonCheckBox.stateChanged.connect(self.cbton_enable_disable)
        self.cbiEnabledCheckBox.stateChanged.connect(self.cbi_enable_disable)

        # Init defaults
        self.cwponCheckBox.setCheckState(2)
        self.cbtonCheckBox.setCheckState(2)
        self.cbiEnabledCheckBox.setCheckState(0)
        self.cbi_enable_disable(0)

        # Calculated results
        self.calc_power = 0.0
        self.calc_data = 0.0
        self.calc_num_batt = 0.0
        self.calc_max_vel = 0.0
        self.calc_std = 0.0
        self.calc_first_bin = 0.0
        self.calc_wp_range = 0.0
        self.calc_bt_range = 0.0


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

        self.cbiBurstIntervaloubleSpinBox.setEnabled(enable_state)
        self.cbiNumEnsSpinBox.setEnabled(enable_state)

    def calculate(self):
        deployment = self.predictor.deploymentDurationspinBox.value()
        cei = self.predictor.ceiDoubleSpinBox.value()
        cws = self.predictor.cwsSpinBox.value()