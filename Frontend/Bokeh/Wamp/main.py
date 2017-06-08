from bokeh.client import push_session
from bokeh.embed import autoload_server
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc

import json

from twisted.logger import Logger
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner

import numpy as np

from Ensemble.Ensemble import Ensemble


class test_bokeh_wamp_1(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        self.amp = None
        self.lastData = None

        self.source = ColumnDataSource(dict(bins=[], AmpB0=[], AmpB1=[]))
        TOOLS = "resize,crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"
        self.fig = figure(x_range=(0, 100), y_range=(0, 120), tools=TOOLS)
        # create a plot and style its properties
        self.fig.border_fill_color = 'black'
        self.fig.background_fill_color = 'black'
        self.fig.outline_line_color = None
        self.fig.grid.grid_line_color = None

        # put the button and plot in a layout and add to the document
        curdoc().add_root(self.fig)

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
        #print(ampNP)
        # Set up data
        #x = np.zeros(4,30)

        bins = []
        ampB0 = []
        ampB1 = []
        velB2 = []
        velB3 = []
        for bin in range(json_data['EnsembleData']["NumBins"]):
            bins.append(bin)
            if Ensemble().is_float_close(json_data['Amplitude']['Amplitude'][bin][0], Ensemble().BadVelocity):
                ampB0.append(json_data['Amplitude']['Amplitude'][bin][0])
            else:
                ampB0.append(0.0)
            if Ensemble().is_float_close(json_data['Amplitude']['Amplitude'][bin][1], Ensemble().BadVelocity):
                ampB1.append(json_data['Amplitude']['Amplitude'][bin][1])
            else:
                ampB1.append(0.0)
            velB2.append(json_data['Amplitude']['Amplitude'][bin][2])
            velB3.append(json_data['Amplitude']['Amplitude'][bin][3])

        new_data = dict(AmpB0=ampB0, AmpB1=ampB1, bins=bins)
        self.source.stream(new_data, 100)
        print(ampB0)



# Start the WAMP connection
# Connect the main window to the WAMP connection
runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1")
runner.run(test_bokeh_wamp_1, auto_reconnect=True)