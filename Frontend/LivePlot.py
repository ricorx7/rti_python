import getopt
import logging
import sys

import matplotlib.pyplot as plt
from matplotlib import cm

from Comm.EnsembleReceiver import EnsembleReceiver

logger = logging.getLogger("EnsembleReceiver")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class LivePlot(EnsembleReceiver):
    """
    Live plot will display live data from the UDP port.
    This inherits from Ensemble Receiver to receive
    and decode the JSON data from the UDP port.
    """

    def __init__(self, udp_port):
        """
        Call the super class to pass the UDP port.
        :param udp_port: UDP Port to read the JSON data.
        """
        #super(LivePlot, self).__init__(udp_port)
        super().__init__()
        self.plot_index = 0
        self.IsBeam = False
        self.IsAmp = False
        self.IsAmpSpline = True

        self.methods = [None, 'none', 'nearest', 'bilinear', 'bicubic', 'spline16',
                   'spline36', 'hanning', 'hamming', 'hermite', 'kaiser', 'quadric',
                   'catrom', 'gaussian', 'bessel', 'mitchell', 'sinc', 'lanczos']

        plt.axis([0, 10, 0, 1])
        plt.ion()

        self.connect(udp_port)




    def process(self, jsonData):
        """
        Process the JSON data that contains the ADCP data.
        :param jsonData: JSON ADCP data.
        :return:
        """
        logger.info(jsonData["Name"])

        if self.IsBeam:
            if "E000001" in jsonData["Name"]:
                #logger.info(self.plot_index)
                #logger.info(jsonData["Velocities"][0][0])
                plt.scatter([self.plot_index, self.plot_index, self.plot_index, self.plot_index], jsonData["Velocities"][0])
                plt.plot(self.plot_index, jsonData["Velocities"][0][1], '--', linewidth=2)
                plt.pause(0.05)
                self.plot_index = self.plot_index + 1

        if self.IsAmp:
            if "E000004" in jsonData["Name"]:
                #plt.scatter([self.plot_index, self.plot_index, self.plot_index, self.plot_index], jsonData["Amplitude"][0])
                plt.scatter(self.plot_index, jsonData["Amplitude"][0][1])
                plt.pause(0.05)
                self.plot_index = self.plot_index + 1

        if self.IsAmpSpline:
            if "E000004" in jsonData["Name"]:
                fig, ax = plt.subplots()
                cax = ax.imshow(jsonData["Amplitude"], interpolation=self.methods[1], cmap=cm.coolwarm, vmin=0, vmax=12)
                ax.set_title('Amplitude Data')
                # Move left and bottom spines outward by 10 points
                ax.spines['left'].set_position(('outward', 10))
                ax.spines['bottom'].set_position(('outward', 10))
                # Hide the right and top spines
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                # Only show ticks on the left and bottom spines
                ax.yaxis.set_ticks_position('left')
                ax.xaxis.set_ticks_position('bottom')

                plt.colorbar(cax)
                plt.xticks(range(0, int(plt.xticks()[0][-1]) + 1, 1))
                plt.pause(0.05)



if __name__ == '__main__':
    argv = sys.argv[1:]
    port = 55057
    try:
        opts, args = getopt.getopt(argv,"p:",["port="])
    except getopt.GetoptError:
        print('LivePlot.py  -p <port>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('LivePlot.py -p <port>')
            sys.exit()
        elif opt in ("-p", "--port"):
            port = int(arg)

    # Read from UDP port
    reader = LivePlot(port)
    reader.close()
    logger.info("Socket Closed")