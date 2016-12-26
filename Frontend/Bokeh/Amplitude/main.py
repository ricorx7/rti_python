from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

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
        self.source = ColumnDataSource(dict(x=[], amp=[]))

        self.lastData = None

        fig = Figure()
        fig.line(source=self.source, x='x', y='amp', line_width=2, alpha=.85, color='red')

        curdoc().add_root(fig)
        curdoc().add_periodic_callback(self.update_data, 1000)

        self.Adcp = ADCP()
        self.t = threading.Thread(target=self.Adcp.connect, args=[55057])
        self.t.start()
        logger.info("init amplitude plot")

    def close(self):
        logger.info("Close plot")

    def update_data(self):
        logger.info("Update plot")
        new_data = dict(x=[self.Adcp.Amplitude["EnsembleNumber"]], amp=[self.Adcp.Amplitude["Amplitude"][0][1]])
        self.source.stream(new_data, 100)


    def process(self, jsonData):
        """
        Process the JSON data that contains the ADCP data.
        :param jsonData: JSON ADCP data.
        :return:
        """
        #logger.info(jsonData["Name"])
        if "E000004" in jsonData["Name"]:
            logger.info(jsonData["Name"])
            new_data = dict(x=[int(jsonData["EnsembleNumber"])], amp=[jsonData["Amplitude"][0]])
            self.source.stream(new_data, 100)
            #self.lastData = jsonData




logger.info("Start Amplitude Plot")
amp = AmplitudeLivePlot(55057)
amp.close()
logger.info("AmplitudeLivePlot Closed")

