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

        bins = []
        ampB0 = []
        ampB1 = []
        ampB2 = []
        ampB3 = []
        corrB0 = []
        corrB1 = []
        corrB2 = []
        corrB3 = []

        for bin in range(json_data['EnsembleData']["NumBins"]):
            bins.append(bin)
            ampB0.append(json_data['Amplitude']["Amplitude"][bin][0])
            ampB1.append(json_data['Amplitude']["Amplitude"][bin][1])
            ampB2.append(json_data['Amplitude']["Amplitude"][bin][2])
            ampB3.append(json_data['Amplitude']["Amplitude"][bin][3])

            corrB0.append(json_data['Correlation']["Correlation"][bin][0])
            corrB1.append(json_data['Correlation']["Correlation"][bin][1])
            corrB2.append(json_data['Correlation']["Correlation"][bin][2])
            corrB3.append(json_data['Correlation']["Correlation"][bin][3])

        self.config.extra['ampB0'].data_source.data["y"] = bins
        self.config.extra['ampB0'].data_source.data["x"] = ampB0

        self.config.extra['ampB1'].data_source.data["y"] = bins
        self.config.extra['ampB1'].data_source.data["x"] = ampB1

        self.config.extra['ampB2'].data_source.data["y"] = bins
        self.config.extra['ampB2'].data_source.data["x"] = ampB2

        self.config.extra['ampB3'].data_source.data["y"] = bins
        self.config.extra['ampB3'].data_source.data["x"] = ampB3

        self.config.extra['corrB0'].data_source.data["y"] = bins
        self.config.extra['corrB0'].data_source.data["x"] = corrB0

        self.config.extra['corrB1'].data_source.data["y"] = bins
        self.config.extra['corrB1'].data_source.data["x"] = corrB1

        self.config.extra['corrB2'].data_source.data["y"] = bins
        self.config.extra['corrB2'].data_source.data["x"] = corrB2

        self.config.extra['corrB3'].data_source.data["y"] = bins
        self.config.extra['corrB3'].data_source.data["x"] = corrB3

if __name__ == '__main__':
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
    tabAmp = Panel(child=ampPlot, title="Amplitude")

    corrPlot = figure(plot_width=600, plot_height=800, tools=TOOLS, x_range=Range1d(0, 1))
    corrPlot.legend.location = "top_left"
    corrPlot.legend.click_policy = "hide"
    corrPlot.xaxis[0].axis_label = "% (percent)"
    corrPlot.yaxis[0].axis_label = "Bin"
    corrB0 = corrPlot.line(x=x, y=y, line_width=2, alpha=.85, color='red', legend="B0")
    corrB1 = corrPlot.line(x=x, y=y, line_width=2, alpha=.85, color='green', legend="B1")
    corrB2 = corrPlot.line(x=x, y=y, line_width=2, alpha=.85, color='blue', legend="B2")
    corrB3 = corrPlot.line(x=x, y=y, line_width=2, alpha=.85, color='orange', legend="B3")
    tabCorr = Panel(child=corrPlot, title="Correlation")

    tabs = Tabs(tabs=[tabAmp, tabCorr])

    # open a session to keep our local document in sync with server
    session = push_session(curdoc())

    session.show(tabs)  # open the document in a browser

    # Start the WAMP connection
    # Connect the main window to the WAMP connection
    runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1",
                               extra={'ampB0': ampB0, 'ampB1': ampB1, 'ampB2': ampB2, 'ampB3': ampB3,
                                      'corrB0': corrB0, 'corrB1': corrB1, 'corrB2': corrB2, 'corrB3': corrB3})
    runner.run(test_bokeh_wamp)

    session.loop_until_closed()  # run forever