from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure, show
from bokeh.client import push_session

from Comm.ADCP import ADCP

import logging
import threading

from Utilities.EnsembleReceiver import EnsembleReceiver

logger = logging.getLogger("EnsembleReceiver")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class AmplitudeLivePlot():

    def __init__(self, udp_port):
        """
        Call the super class to pass the UDP port.
        :param udp_port: UDP Port to read the JSON data.
        """
        #super(LivePlot, self).__init__(udp_port)
        super().__init__()
        #self.source = ColumnDataSource(dict(bins=[], ampB0=[], ampB1=[]))

        self.bins = []
        self.ampB0 = []
        self.ampB1 = []
        self.ampB2 = []
        self.ampB3 = []


        self.fig = Figure()
        #self.l1 = fig.line(source=self.source, x='ampB0', y='bins', line_width=2, alpha=.85, color='red')
        #self.l2 = fig.line(source=self.source, x='ampB1', y='bins', line_width=2, alpha=.85, color='blue')
        self.l1 = self.fig.line(x=self.ampB0, y=self.bins, line_width=2, alpha=.85, color='red')
        self.l2 = self.fig.line(x=self.ampB1, y=self.bins, line_width=2, alpha=.85, color='blue')

        #curdoc().add_root(fig)
        #curdoc().add_periodic_callback(self.update_data, 500)

        session = push_session(curdoc())

        self.Adcp = ADCP()
        self.t = threading.Thread(target=self.Adcp.connect, args=[55057])
        self.t.start()
        logger.info("init amplitude plot")

        curdoc().add_periodic_callback(self.update_data, 500)

        session.show(self.fig)
        session.loop_until_closed()

    def close(self):
        logger.info("Close plot")
        self.Adcp.close()

    def update_data(self):
        if self.Adcp.EnsembleData is None or self.Adcp.Amplitude is None:
            pass

        logger.info("Update plot")

        self.bins = []
        self.ampB0 = []
        self.ampB1 = []
        self.ampB2 = []
        self.ampB3 = []

        for bin in range(self.Adcp.EnsembleData["NumBins"]):
            self.bins.append(bin)
            self.ampB0.append(self.Adcp.Amplitude["Amplitude"][bin][0])
            self.ampB1.append(self.Adcp.Amplitude["Amplitude"][bin][1])
            self.ampB2.append(self.Adcp.Amplitude["Amplitude"][bin][2])
            self.ampB3.append(self.Adcp.Amplitude["Amplitude"][bin][3])

        #print(bins)
        #print(ampB0)

        #new_data = dict(x=[self.Adcp.Amplitude["EnsembleNumber"]], amp=[self.Adcp.Amplitude["Amplitude"][0][1]])
        #new_data = dict(ampB0=ampB0, ampB1=ampB1, bins=bins)
        #self.source.stream(new_data, 100)
        self.l1.data_source.data["y"] = self.ampB0
        self.l2.data_source.data["y"] = self.ampB1




logger.info("Start Amplitude Plot")
amp = AmplitudeLivePlot(55057)
#amp.close()
logger.info("AmplitudeLivePlot Closed")

