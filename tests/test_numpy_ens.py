import json

from twisted.logger import Logger
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner

import numpy as np
import pandas as pd

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
        self.amp = json_data['Amplitude']                                                           # Get the amplitude data
        amp_np = np.array(json_data['Amplitude']['Amplitude'])                                      # Create a numpy array from the amplitude data
        df = pd.DataFrame(columns=['AmpB0', 'AmpB1', 'AmpB2', 'AmpB3'], data=amp_np)                # Create a description(name) for the columns

        corr_np = np.array(json_data['Correlation']['Correlation'])                                 # Get the correlation data
        corr_df = pd.DataFrame(columns=['CorrB0', 'CorrB1', 'CorrB2', 'CorrB3'], data=corr_np)      # Create a numpy array from the correlation data
        corr_scale = lambda x: x*100                                                                # Mulitply by 100 to make percent
        corr_df = corr_df.applymap(corr_scale)  # Scale from 0% to 100%                             # Apply lambda function

        df = df.join(corr_df)                                                                       # Combine the amplitude and correlation dataframe
        print(df.shape)
        print(df)



if __name__ == '__main__':
    # Start the WAMP connection
    # Connect the main window to the WAMP connection
    runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1")
    runner.run(test_numpy_ens, auto_reconnect=True)