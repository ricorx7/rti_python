import json

from twisted.logger import Logger
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner

import numpy as np

class test_numpy_ens(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        self.amp = None


    @inlineCallbacks
    def onJoin(self, details):
        """
        Initialize the WAMP settings.  This is called before everything is setup to ensure
        the WAMP settings are initialized.
        :return:
        """
        self.log.info("WAMP connected")

        yield self.subscribe(self.on_ens_json_data, u"com.rti.data.ens")
        self.log.info("test Numpy WAMP init")

    def on_ens_json_data(self, data):
        """
        Called when JSON Ensemble data is received from WAMP.
        :param data: JSON object containing serial data.
        :return:
        """
        json_data = json.loads(data)                        # convert to JSON
        self.amp = json_data['Amplitude']
        #print(self.amp['Amplitude'])
        ampBin1 = json_data['Amplitude']['Amplitude']
        #print(ampBin1[0])
        ampNP = np.array(json_data['Amplitude']['Amplitude'])
        print(ampNP)

if __name__ == '__main__':
    # Start the WAMP connection
    # Connect the main window to the WAMP connection
    runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1")
    runner.run(test_numpy_ens, auto_reconnect=True)