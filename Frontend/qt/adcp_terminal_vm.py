from adcp_terminal_view import Ui_AdcpTerminal
from twisted.internet.defer import inlineCallbacks

import json

class AdcpTerminal(Ui_AdcpTerminal):

    def __init__(self, parent):
        Ui_AdcpTerminal.__init__(self)
        self.setupUi(parent)
        self.parent = parent

        # Connect "BREAK" button with a custom function
        self.breakButton.clicked.connect(self.send_break)
        self.sendButton.clicked.connect(self.send_cmd)

    @inlineCallbacks
    def wamp_init(self):
        yield self.parent.subscribe(self.on_serial_data, u"com.rti.data.serial")
        yield self.parent.subscribe(self.on_serial_list, u'com.rti.serial.list')
        self.parent.call(u'com.rti.serial.list.get', [])
        self.parent.log.info("ADCP Terminal WAMP init")

    def send_break(self):
        # Call to WAMP for a BREAK
        self.parent.call(u"com.rti.onbreak", [100])

    def send_cmd(self):
        # Call to WAMP for a command
        self.parent.call(u"com.rti.oncmd", self.cmdLineText.text())
        self.cmdLineText.setText("")

    def on_serial_data(self, data):
        # Receiver serial data from subscription
        self.terminalText.setText(data)

    def on_serial_list(self, data):
        # Receive serial port list from subscription
        self.terminalText.setText(data)


