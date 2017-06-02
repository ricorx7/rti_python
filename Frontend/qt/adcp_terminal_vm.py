from adcp_terminal_view import Ui_AdcpTerminal
from twisted.internet.defer import inlineCallbacks

import json
import sys
import glob
from PyQt5 import QtCore


class AdcpTerminal(Ui_AdcpTerminal):
    """
    ADCP Terminal using WAMP.
    """

    def __init__(self, parent):
        Ui_AdcpTerminal.__init__(self)
        self.setupUi(parent)
        self.parent = parent

        self.serial_settings_checked = False

        # Connect "BREAK" button with a custom function
        self.breakButton.clicked.connect(self.send_break)
        self.sendButton.clicked.connect(self.send_cmd)
        self.serialConnectButton.clicked.connect(self.send_connect)

        # Set the list of serial ports and baud rates
        self.set_serialport_list()
        self.set_baudrate_list()

    @inlineCallbacks
    def wamp_init(self):
        """
        Initialize the WAMP settings.  This is called before everything is setup to ensure
        the WAMP settings are initialized.
        :return: 
        """
        yield self.parent.subscribe(self.on_serial_data, u"com.rti.data.serial")
        yield self.parent.subscribe(self.on_ens_json_data, u"com.rti.data.ens")
        self.parent.log.info("ADCP Terminal WAMP init")

    def send_break(self):
        """
        Send a BREAK to WAMP for the serial port.
        :return: 
        """
        # Call to WAMP for a BREAK
        self.parent.call(u"com.rti.onbreak", [100])

    def send_cmd(self):
        """
        Send a command to WAMP for the serial port.
        :return: 
        """
        # Call to WAMP for a command
        self.parent.call(u"com.rti.oncmd", self.cmdLineText.text())
        self.cmdLineText.setText("")

    def send_connect(self):
        """
        Call the Reconnect to change the connection of the serial port.
        :return: 
        """
        self.parent.call(u'com.rti.serial.reconnect', str(self.serialPortcomboBox.currentText()), str(self.baudRatecomboBox.currentText()))

    def on_serial_data(self, data):
        """
        Called when serial data is received from WAMP.
        :param data: JSON object containing serial data.
        :return: 
        """
        json_data = json.loads(data)                        # convert to JSON
        self.check_serial_settings(json_data)               # Check serial settings
        self.terminalText.append(str(json_data["value"]))  # Set terminal output

        # Keep the size of the terminal text buffer small
        term_txt = str(self.terminalText.toPlainText())
        if len(term_txt) > 1030:
            self.terminalText.setText(term_txt[len(term_txt) - 1030:])

    def on_ens_json_data(self, data):
        """
        Called when JSON Ensemble data is received from WAMP.
        :param data: JSON object containing serial data.
        :return: 
        """
        json_data = json.loads(data)                        # convert to JSON
        self.check_serial_settings(json_data)               # Check serial settings
        self.ensJsonText.setText(str(json_data['EnsembleData']))
        #self.ensJsonText.append(str(json_data["value"]))  # Set terminal output

        # Keep the size of the terminal text buffer small
        #ens_json_txt = str(self.ensJsonText.toPlainText())
        #if len(ens_json_txt) > 1030:
        #    self.ensJsonText.setText(ens_json_txt[len(ens_json_txt) - 1030:])

    def check_serial_settings(self, json_data):
        """
        Make the serial port option match the incoming data.
        The serial port is obvious connected if data is coming in, so make the settings match.
        :param json_data: JSON data to get the settings.
        :return: 
        """
        # Do this only once on startup
        if not self.serial_settings_checked:
            self.serial_settings_checked = True
            # Check baud rate
            if self.baudRatecomboBox.currentText != str(json_data["baud"]):
                index = self.baudRatecomboBox.findText(str(json_data["baud"]), QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.baudRatecomboBox.setCurrentIndex(index)

            # Check serial port
            if self.serialPortcomboBox.currentText != json_data["port"]:
                index = self.serialPortcomboBox.findText(json_data["port"], QtCore.Qt.MatchFixedString)
                if index >= 0:
                    self.serialPortcomboBox.setCurrentIndex(index)

    def set_serialport_list(self):
        """
        Set the serial port list.
        :return: 
        """
        # Receive serial port list from subscription
        self.serialPortcomboBox.addItems(self.list_serial_ports())

    def set_baudrate_list(self):
        """
        Set the baud rate list.
        :return: 
        """
        bauds = ["921600", "460800", "230400", "115200", "38400", "19200", "9600", "4800", "2400"]
        self.baudRatecomboBox.addItems(bauds)

    def list_serial_ports(self):
        """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = ports

        return result
