import os.path
import sys
import getopt
import folium
from log import logger
from Codecs.AdcpCodec import AdcpCodec


class waypoint_creator:

    def __init__(self):


        # Codec to decode the data from the file
        self.codec = AdcpCodec(55057)
        self.codec.EnsembleEvent += self.process_ensemble_codec

        self.map_osm = None

        self.ens_codec_count = 0

    def process(self, file_path):
        """
        Read the file and start a thread to monitor the incoming ensembles.
        :param file_path: File  path the read files
        :return:
        """

        # Process the file
        self.process_file(file_path)

        self.map_osm.save('osm.html')

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
        if ens.IsNmeaData:
            if ens.NmeaData.GPGGA is not None:
                if self.map_osm is None:
                    self.map_osm = folium.Map(location=[ens.NmeaData.GPGGA.latitude, ens.NmeaData.GPGGA.longitude], zoom_start=16)

                marker_msg = "Lat: " + str(ens.NmeaData.GPGGA.latitude) + " Lon:" + str(ens.NmeaData.GPGGA.longitude)

                folium.Marker([ens.NmeaData.GPGGA.latitude, ens.NmeaData.GPGGA.longitude], popup=marker_msg).add_to(self.map_osm)
                #print(ens.NmeaData.GPGGA)
                #print(ens.NmeaData.GPGGA.latitude)


def main(argv):
    inputfile = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv,"hvi:",["ifile=","verbose"])
    except getopt.GetoptError:
        print('test_display_waypoints.py -i <inputfile> -v')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test_display_waypoints.py -i <inputfile> -v')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
            print("Verbose ON")
    print('Input file is: ', inputfile)

    # Read the file and process all the waypoints
    waypoint_creator().process(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])