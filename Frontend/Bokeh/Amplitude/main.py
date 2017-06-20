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
import pandas as pd

class test_bokeh_wamp(ApplicationSession):

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        self.df = None

        x = np.array([1])
        y = np.array([1])
        TOOLS = 'pan,box_zoom,wheel_zoom,box_select,crosshair,resize,reset,save,hover'
        ampPlot = figure(plot_width=600, plot_height=800, tools=TOOLS, x_range=Range1d(0, 140))
        ampPlot.legend.location = "top_left"
        ampPlot.legend.click_policy = "hide"
        ampPlot.xaxis[0].axis_label = "dB"
        ampPlot.yaxis[0].axis_label = "Bin"
        self.ampB0 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='red', legend="B0")
        self.ampB1 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='green', legend="B1")
        self.ampB2 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='blue', legend="B2")
        self.ampB3 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='orange', legend="B3")
        curdoc().add_root(ampPlot)

    @inlineCallbacks
    def onJoin(self, details):
        """
        Initialize the WAMP settings.  This is called before everything is setup to ensure
        the WAMP settings are initialized.
        :return:
        """
        self.log.info("WAMP connected")

        yield self.subscribe(self.on_ens_json_data, u"com.rti.data.ens")
        self.log.info("test Amplitude Bokeh WAMP init")

    def on_ens_json_data(self, data):
        """
        Called when JSON Ensemble data is received from WAMP.
        :param data: JSON object containing serial data.
        :return:
        """
        json_data = json.loads(data)                        # convert to JSON
        self.amp = json_data['Amplitude']                                                           # Get the amplitude data
        amp_np = np.array(json_data['Amplitude']['Amplitude'])                                      # Create a numpy array from the amplitude data
        self.df = pd.DataFrame(columns=['AmpB0', 'AmpB1', 'AmpB2', 'AmpB3'], data=amp_np)                # Create a description(name) for the columns
        print("-")

    def callback(self):
        self.ampB0.data_source.data["y"] = self.df.index
        self.ampB0.data_source.data["x"] = self.df.loc[:, 'AmpB0']

        self.ampB1.data_source.data["y"] = self.df.index
        self.ampB1.data_source.data["x"] = self.df.loc[:, 'AmpB1']

        self.ampB2.data_source.data["y"] = self.df.index
        self.ampB2.data_source.data["x"] = self.df.loc[:, 'AmpB2']

        self.ampB3.data_source.data["y"] = self.df.index
        self.ampB3.data_source.data["x"] = self.df.loc[:, 'AmpB3']
        print(".")

#x = np.array([1])
#y = np.array([1])
#TOOLS = 'pan,box_zoom,wheel_zoom,box_select,crosshair,resize,reset,save,hover'
#ampPlot = figure(plot_width=600, plot_height=800, tools=TOOLS, x_range=Range1d(0, 140))
#ampPlot.legend.location = "top_left"
#ampPlot.legend.click_policy = "hide"
#ampPlot.xaxis[0].axis_label="dB"
#ampPlot.yaxis[0].axis_label = "Bin"
#ampB0 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='red', legend="B0")
#ampB1 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='green', legend="B1")
#ampB2 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='blue', legend="B2")
#ampB3 = ampPlot.line(x=x, y=y, line_width=2, alpha=.85, color='orange', legend="B3")

# open a session to keep our local document in sync with server
#session = push_session(curdoc())

#session.show(ampPlot)  # open the document in a browser

#tbw = test_bokeh_wamp()

#curdoc().add_root(ampPlot)
#curdoc().add_periodic_callback(tbw.callback, 1000)

# Start the WAMP connection
# Connect the main window to the WAMP connection
#runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1",
#                           extra={'ampB0': ampB0, 'ampB1': ampB1, 'ampB2': ampB2, 'ampB3': ampB3})


runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1")
runner.run(test_bokeh_wamp, start_reactor=True)

#from twisted.internet import reactor
#reactor.run()
#session.loop_until_closed()  # run forever

