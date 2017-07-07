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

class PlotMagnitude:

    def __init__(self):
        self.ens_receiver = None
        self.ens_reader = None

        # Codec to decode the data from the file
        self.codec = AdcpCodec(is_udp=False)
        self.codec.EnsembleEvent += self.process_ensemble_codec

        self.ens_codec_count = 0

        sns.plt.axis([0, 10, 0, 1])
        sns.plt.ion()

        self.fig = sns.plt.figure()
        self.ax = self.fig.add_subplot(111)  # Create an axes.
        sns.plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)

        # Flag to display the colorbar only once
        self.cbar_display = True

        self.mag_df = None

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

            # Plot final results
            sns.heatmap(self.mag_df, cbar=self.cbar_display)                        # Set flag to only display colorbar once
            sns.plt.pause(0.000001)                                                   # Pause to refresh the display
            self.cbar_display = False

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
            df = pd.DataFrame(columns=['East', 'North', 'Vertical', 'Error'], data=earthVel_np)  # Create a description(name) for the columns
            print(df[:75])
            #print(df.shape)

            # Add Magnitude and Direction to the dataframe
            df["mag"] = 0
            df["dir"] = 0
            #df.index.name = "index"
            for index, row in df.iterrows():
                east = row["East"]
                north = row["North"]
                vert = row["Vertical"]
                mag = 0.0
                dir = 0.0
                # Calculate the mag and dir if the data is good
                if not math.isclose(east, Ensemble.Ensemble.BadVelocity, rel_tol=0.001, abs_tol=0.001) and \
                        not math.isclose(north, Ensemble.Ensemble.BadVelocity, rel_tol=0.001, abs_tol=0.001) and \
                        not math.isclose(vert, Ensemble.Ensemble.BadVelocity, rel_tol=0.001, abs_tol=0.001):
                    mag = math.sqrt(math.pow(east, 2) + math.pow(north, 2) + math.pow(vert, 2))
                    dir = math.atan2(north, east) * (180.0 / math.pi)
                    df.loc[index, "mag"] = mag
                    df.loc[index, "dir"] = dir

            #print(df)

            # Line
            #self.ax.cla()                       # Clear the axis so it will not repopulate the list
            #df.plot(ax=self.ax, y="mag")        # Set y to the column to plot,  Pass the axes to plot.
            #plt.draw()                          # Draw instead of show to update the plot in ion mode.
            #plt.pause(0.0001)                    # Pause the plot so it can refreshed and seen

            # Heatmap
            #piv = pd.pivot_table(df, values="mag", index=df.index)          # Create pivot table to just get 1 column of data
            #sns.heatmap(piv, cbar=self.cbar_display)                        # Set flag to only display colorbar once
            #sns.plt.pause(0.0001)
            #self.cbar_display = False

            # Create a temp dataframe
            # Then combine it with the master dataframe
            df_mag = pd.DataFrame(columns=[str(ens.EnsembleData.EnsembleNumber)], index=df.index)
            df_mag[str(ens.EnsembleData.EnsembleNumber)] = df['mag']
            #print(df_mag)
            if self.mag_df is None:
                self.mag_df = df_mag                                                # Create the initial dataframe
            else:
                self.mag_df = pd.concat([self.mag_df, df_mag], axis=1)              # Combine the dataframes into one large one
            #print(self.mag_df)

            # Live Plot
            #sns.heatmap(self.mag_df, cbar=self.cbar_display)                        # Set flag to only display colorbar once
            #sns.plt.pause(0.000001)                                                   # Pause to refresh the display
            #self.cbar_display = False

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


