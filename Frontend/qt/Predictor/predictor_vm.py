from predictor_view import Ui_RoweTechPredictor
from subsystem_view import Ui_Subsystem
from subsystem_vm import SubsystemVM
from PyQt5.QtWidgets import QWidget


class PredictorVM(Ui_RoweTechPredictor):
    """
    ADCP Terminal using WAMP.
    """

    def __init__(self, parent):
        Ui_RoweTechPredictor.__init__(self)
        self.setupUi(parent)
        self.parent = parent

        # Connect the buttons
        self.addSubsystemButton.clicked.connect(self.add_subsystem)

        self.tabSubsystem.setTabsClosable(True)
        self.tabSubsystem.clear()
        self.tabSubsystem.tabCloseRequested.connect(self.tab_close_requested)
        self.calculateButton.clicked.connect(self.calculate)

        # Create the list of subsystems
        self.init_list()

    def init_list(self):
        # Add item to combobox.  Set the userData to subsystem code
        self.subsystemComboBox.addItem("2 - 1200kHz", "2")
        self.subsystemComboBox.addItem("3 - 600kHz", "3")
        self.subsystemComboBox.addItem("4 - 300kHz", "4")
        self.subsystemComboBox.addItem("6 - 1200kHz 45 degree offset", "6")
        self.subsystemComboBox.addItem("7 - 600kHz 45 degree offset", "7")
        self.subsystemComboBox.addItem("8 - 300kHz 45 degree offset", "8")
        self.subsystemComboBox.addItem("A - 1200kHz Vertical", "A")
        self.subsystemComboBox.addItem("B - 600kHz Vertical", "B")
        self.subsystemComboBox.addItem("C - 300kHz Vertical", "C")
        self.subsystemComboBox.addItem("D - 150kHz Vertical", "D")
        self.subsystemComboBox.addItem("E - 75kHz Vertical", "E")

    def add_subsystem(self):
        """
        Add a tab for the given subsystem.
        :return:
        """
        ss = self.subsystemComboBox.itemData(self.subsystemComboBox.currentIndex())

        # Create the subsystem view
        # Add it to the Tab
        ssUI = Ui_Subsystem()
        ssVM = SubsystemVM(self.tabSubsystem, self)
        self.tabSubsystem.addTab(ssVM, ss)

    def tab_close_requested(self, index):
        """
        Remove the tab.
        :param index: Index of the tab.
        :return:
        """
        self.tabSubsystem.removeTab(index)

    def calculate(self):
        print(self.tabSubsystem.count())
        for tab in range(self.tabSubsystem.count()):
            self.tabSubsystem.widget(tab).calculate()
            print(self.tabSubsystem.widget(tab).cwpblDoubleSpinBox.value())
