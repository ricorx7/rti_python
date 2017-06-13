import json

from twisted.logger import Logger
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner

from bokeh.client import push_session
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import Range1d

import numpy as np

class test_bokeh_wamp(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)

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
        print(".")
        bins = []
        ampB0 = []
        ampB1 = []
        ampB2 = []
        ampB3 = []

        for bin in range(json_data['EnsembleData']["NumBins"]):
            bins.append(bin)
            ampB0.append(json_data['Amplitude']["Amplitude"][bin][0])
            ampB1.append(json_data['Amplitude']["Amplitude"][bin][1])
            ampB2.append(json_data['Amplitude']["Amplitude"][bin][2])
            ampB3.append(json_data['Amplitude']["Amplitude"][bin][3])

        self.config.extra['ampB0'].data_source.data["y"] = bins
        self.config.extra['ampB0'].data_source.data["x"] = ampB0

        self.config.extra['ampB1'].data_source.data["y"] = bins
        self.config.extra['ampB1'].data_source.data["x"] = ampB1

        self.config.extra['ampB2'].data_source.data["y"] = bins
        self.config.extra['ampB2'].data_source.data["x"] = ampB2

        self.config.extra['ampB3'].data_source.data["y"] = bins
        self.config.extra['ampB3'].data_source.data["x"] = ampB3


x = np.array([1])
y = np.array([1])
TOOLS = 'pan,box_zoom,wheel_zoom,box_select,crosshair,resize,reset,save,hover'
ampPlot = figure(plot_width=600, plot_height=800, tools=TOOLS, x_range=Range1d(0, 140))
ampPlot.legend.location = "top_left"
ampPlot.legend.click_policy = "hide"
ampPlot.xaxis[0].axis_label="dB"
ampPlot.yaxis[0].axis_label = "Bin"
ampB0 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='red', legend="B0")
ampB1 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='green', legend="B1")
ampB2 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='blue', legend="B2")
ampB3 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='orange', legend="B3")

# open a session to keep our local document in sync with server
#session = push_session(curdoc())

#session.show(ampPlot)  # open the document in a browser

curdoc().add_root(ampPlot)

# Start the WAMP connection
# Connect the main window to the WAMP connection
runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1",
                           extra={'ampB0': ampB0, 'ampB1': ampB1, 'ampB2': ampB2, 'ampB3': ampB3})
runner.run(test_bokeh_wamp)


#session.loop_until_closed()  # run forever