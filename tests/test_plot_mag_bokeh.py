import os.path
import sys
import getopt
import math
import pandas as pd
import numpy as np
from log import logger
from Codecs.AdcpCodec import AdcpCodec
import Ensemble.Ensemble as Ensemble

import matplotlib.pyplot as plt
import seaborn as sns

from bokeh.charts import HeatMap, output_file, show
from bokeh.models import Range1d, HoverTool
from bokeh.plotting import figure

class PlotMagnitude:

    def __init__(self):
        self.ens_receiver = None
        self.ens_reader = None

        # Codec to decode the data from the file
        self.codec = AdcpCodec(is_udp=False)
        self.codec.EnsembleEvent += self.process_ensemble_codec

        self.ens_codec_count = 0

        # Create a dataframe to hold a rowe for every bin
        self.df_mag_ens = pd.DataFrame(data=None, columns=['bin', 'ens', 'mag', 'dir'])

    def process(self, file_path):
        """
        Read the file and start a thread to monitor the incoming ensembles.
        :param file_path: File  path the read files
        :return:
        """

        # Process the file
        self.process_file(file_path)

        logger.info("Completed File reader")
        logger.info("Ensemble Codec Count: " + str(self.ens_codec_count))

    def process_file(self, file_path):
        """
        Process the file given.  This read from the file
        and add it to the codec.  The codec will then decode
        the data and pass it to the UDP port.
        """
        # Check if the file exist
        if os.path.exists(file_path):

            logger.info("Open file: " + file_path)

            # Open the file
            f = open(file_path, "rb")

            # Add the data from the file to the codec
            data = f.read(4096)
            while len(data) > 0:
                # Add data to codec
                self.codec.add(data)

                # Read next block from the file
                data = f.read(4096)

            # Close the file
            f.close()

            # Display the Heatmap and save it to HTML file
            output_file('test.html')

            hover = HoverTool(tooltips=[
                ("index", "$index"),
                ("(x,y)", "($x, $y)"),
                ("desc", "@desc"),
            ])

            hm = HeatMap(self.df_mag_ens, x='ens', y='bin', values='mag',
                         stat=None,
                         sort_dim={'x': False},
                         width=1000,
                         spacing_ratio=0.9,
                         tools=[hover],
                         toolbar_location="above",          # Move toolbar to top
                         toolbar_sticky=False)              # Make toolbar not to close to plot

            # Set min and max axis and invert axis
            xmin = self.df_mag_ens['ens'].min()
            xmax = self.df_mag_ens['ens'].max()
            ymax = self.df_mag_ens['bin'].min()         # Swap Min and Max for y axis
            ymin = self.df_mag_ens['bin'].max()         # Swap Min and Max for y axis
            hm.x_range = Range1d(xmin, xmax)            # Set the min and max, so no gaps on edges
            hm.y_range = Range1d(ymin, ymax)            # Set the min and max, so no gaps on edges
            show(hm)

            while True:
                input("Press enter to continue")
                break

        else:
            logger.error("File does not exist")

    def process_ensemble_codec(self, sender, ens):
        """
        Receive and process the incoming ensemble directly from the codec.
        This data was process and passed as an Ensemble object.
        :param sender: Sender of the ensemble.
        :param ens: Ensemble data.
        """
        if ens.IsEnsembleData:
            #print("Codec: " + str(ens.EnsembleData.EnsembleNumber))
            self.ens_codec_count += 1

        if ens.IsEarthVelocity:
            #print(len(ens.EarthVelocity.Velocities))
            earthVel_np = np.array(ens.EarthVelocity.Velocities)                                 # Create Numpy array for the velocity data
            #earthVel_np = np.array(ens.BeamVelocity.Velocities)
            df = pd.DataFrame(columns=['east', 'north', 'vertical', 'error'], data=earthVel_np)  # Create a description(name) for the columns


            for index, row in df.iterrows():
                east = row["east"]
                north = row["north"]
                vert = row["vertical"]
                # Calculate the mag and dir if the data is good
                if not math.isclose(east, Ensemble.Ensemble.BadVelocity, rel_tol=0.001, abs_tol=0.001) and \
                        not math.isclose(north, Ensemble.Ensemble.BadVelocity, rel_tol=0.001, abs_tol=0.001) and \
                        not math.isclose(vert, Ensemble.Ensemble.BadVelocity, rel_tol=0.001, abs_tol=0.001):
                    mag = math.sqrt(math.pow(east, 2) + math.pow(north, 2) + math.pow(vert, 2))
                    dir = math.atan2(north, east) * (180.0 / math.pi)

                    # Add a row for every bin
                    self.df_mag_ens.loc[len(self.df_mag_ens)] = [index, ens.EnsembleData.EnsembleNumber, mag, dir]


def main(argv):
    inputfile = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv,"hvi:",["ifile=","verbose"])
    except getopt.GetoptError:
        print('PlotMagnitude.py -i <inputfile> -v')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('PlotMagnitude.py -i <inputfile> -v')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
            print("Verbose ON")
    print('Input file is: ', inputfile)

    # Run report on file
    PlotMagnitude().process(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])


