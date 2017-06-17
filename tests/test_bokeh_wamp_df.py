import json
import sys

from twisted.logger import Logger
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner

from bokeh.client import push_session
from bokeh.plotting import figure, curdoc
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import Range1d

from Frontend.qt.test.browser import Browser
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl

import numpy as np
import pandas as pd

class test_bokeh_wamp_df(ApplicationSession):

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
        self.log.info("test Bokehs WAMP init")

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
        #print(df.shape)
        #print(df)

        self.config.extra['ampB0'].data_source.data["y"] = df.index
        self.config.extra['ampB0'].data_source.data["x"] = df.loc[:, 'AmpB0']

        self.config.extra['ampB1'].data_source.data["y"] = df.index
        self.config.extra['ampB1'].data_source.data["x"] = df.loc[:, 'AmpB1']

        self.config.extra['ampB2'].data_source.data["y"] = df.index
        self.config.extra['ampB2'].data_source.data["x"] = df.loc[:, 'AmpB2']

        self.config.extra['ampB3'].data_source.data["y"] = df.index
        self.config.extra['ampB3'].data_source.data["x"] = df.loc[:, 'AmpB3']

        self.config.extra['corrB0'].data_source.data["y"] = df.index
        self.config.extra['corrB0'].data_source.data["x"] = df.loc[:, 'CorrB0']

        self.config.extra['corrB1'].data_source.data["y"] = df.index
        self.config.extra['corrB1'].data_source.data["x"] = df.loc[:, 'CorrB1']

        self.config.extra['corrB2'].data_source.data["y"] = df.index
        self.config.extra['corrB2'].data_source.data["x"] = df.loc[:, 'CorrB2']

        self.config.extra['corrB3'].data_source.data["y"] = df.index
        self.config.extra['corrB3'].data_source.data["x"] = df.loc[:, 'CorrB3']

        # self.config.extra['corrB3'].y_range = Range1d(df.index.max, df.index.min)       # Invert axis


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

    corrPlot = figure(plot_width=600, plot_height=800, tools=TOOLS, x_range=Range1d(0, 100))
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

    doc = curdoc()
    doc.title = "Amplitude and Correlation Plot"

    # open a session to keep our local document in sync with server
    session = push_session(doc)
    print("Session ID: ", session)

    session.show(tabs)  # open the document in a browser

    app = QApplication(sys.argv)
    brow = Browser()
    brow.setUrl(QUrl("http://localhost:5006/?bokeh-session-id=" + str(session.id)))
    brow.setMinimumHeight(900)
    brow.show()

    import qt5reactor
    # Add PyQT5 to twisted reactor
    qt5reactor.install()

    # Start the WAMP connection
    # Connect the main window to the WAMP connection
    runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1",
                               extra={'ampB0': ampB0, 'ampB1': ampB1, 'ampB2': ampB2, 'ampB3': ampB3,
                                      'corrB0': corrB0, 'corrB1': corrB1, 'corrB2': corrB2, 'corrB3': corrB3})
    runner.run(test_bokeh_wamp_df)

    session.loop_until_closed()  # run forever