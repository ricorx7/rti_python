import logging
import threading

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure

from Comm.EnsembleJsonData import ADCP
from Ensemble.Ensemble import Ensemble

logger = logging.getLogger("EnsembleReceiver")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class BeamVelocityLivePlot:
    """
    Plot Beam Velocity data live using Bokeh server.

    bokeh serve .
    """

    def __init__(self, udp_port):
        """
        Call the super class to pass the UDP port.
        :param udp_port: UDP Port to read the JSON data.
        """
        #super(LivePlot, self).__init__(udp_port)
        super().__init__()
        self.source = ColumnDataSource(dict(bins=[], beamVelB0=[], beamVelB1=[]))

        self.lastData = None

        fig = Figure()
        fig.line(source=self.source, x='beamVelB0', y='bins', line_width=2, alpha=.85, color='red')
        fig.line(source=self.source, x='beamVelB1', y='bins', line_width=2, alpha=.85, color='blue')


        curdoc().add_root(fig)
        curdoc().add_periodic_callback(self.update_data, 200)

        self.Adcp = ADCP()
        self.t = threading.Thread(target=self.Adcp.connect, args=[55057])
        self.t.start()
        logger.info("init Beam Velocity plot")

    def close(self):
        logger.info("Close plot")
        self.Adcp.close()

    def update_data(self):
        #logger.info("Update plot")

        if self.Adcp.EnsembleData is None and self.Adcp.BeamVelocity is None:
            pass

        bins = []
        velB0 = []
        velB1 = []
        velB2 = []
        velB3 = []
        for bin in range(self.Adcp.EnsembleData["NumBins"]):
            bins.append(bin)
            if Ensemble().is_float_close(self.Adcp.BeamVelocity["Velocities"][bin][0], Ensemble().BadVelocity):
                velB0.append(self.Adcp.BeamVelocity["Velocities"][bin][0])
            else:
                velB0.append(0.0)
            if Ensemble().is_float_close(self.Adcp.BeamVelocity["Velocities"][bin][1], Ensemble().BadVelocity):
                velB1.append(self.Adcp.BeamVelocity["Velocities"][bin][1])
            else:
                velB1.append(0.0)
            velB2.append(self.Adcp.BeamVelocity["Velocities"][bin][2])
            velB3.append(self.Adcp.BeamVelocity["Velocities"][bin][3])

        #new_data = dict(x=[self.Adcp.Amplitude["EnsembleNumber"]], amp=[self.Adcp.Amplitude["Amplitude"][0][1]])
        new_data = dict(beamVelB0=velB0, beamVelB1=velB1, bins=bins)
        self.source.stream(new_data, 100)




logger.info("Start Beam Velocity Plot")
amp = BeamVelocityLivePlot(55057)
#amp.close()
logger.info("Beam Velocity Plot Closed")

