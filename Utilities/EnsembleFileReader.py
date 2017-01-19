import os.path
import sys
import getopt
import threading
import json
from log import logger
from Comm.EnsembleReceiver import EnsembleReceiver
from Codecs.AdcpCodec import AdcpCodec


class EnsembleFileReader:

    def __init__(self):
        self.ens_receiver = None
        self.ens_reader = None

        # Codec to decode the data from the file
        self.codec = AdcpCodec(55057)
        self.codec.EnsembleEvent += self.process_ensemble_codec

        self.ens_count = 0
        self.ens_codec_count = 0

    def process(self, file_path):
        """
        Read the file and start a thread to monitor the incoming ensembles.
        :param file_path: File  path the read files
        :return:
        """

        # Create ensemble receiver
        self.ens_receiver = EnsembleReceiver()
        self.ens_receiver.EnsembleEvent += self.process_ensemble

        # Start thread to monitor incoming ensembles
        # Connect to ensemble server
        self.ens_reader = threading.Thread(name='EnsFileReader', target=self.ens_receiver.connect, args=[55057]).start()

        # Process the file
        self.process_file(file_path)

        # Stop the receiver
        self.ens_receiver.close()

        logger.info("Completed File reader")
        logger.info("Ensemble UDP Count: " + str(self.ens_count))
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

    def process_ensemble(self, sender, ens):
        """
        Receive and process the incoming ensemble from the UDP port.
        This data has been processed through the codec then passed over
        the UDP port as JSON data.  The JSON datasets were then collected
        and assembled as a JSON ensemble.
        :param sender: Sender of the ensemble.
        :param ens: Ensemble data.
        """
        print("UDP: " + str(ens.EnsembleNumber))
        self.ens_count += 1

    def process_ensemble_codec(self, sender, ens):
        """
        Receive and process the incoming ensemble directly from the codec.
        This data was process and passed as an Ensemble object.
        :param sender: Sender of the ensemble.
        :param ens: Ensemble data.
        """
        if ens.IsEnsembleData:
            print("Codec: " + str(ens.EnsembleData.EnsembleNumber))
            self.ens_codec_count += 1





def main(argv):
    inputfile = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv,"hvi:",["ifile=","verbose"])
    except getopt.GetoptError:
        print('EnsembleFileReader.py -i <inputfile> -v')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('EnsembleFileReader.py -i <inputfile> -v')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
            print("Verbose ON")
    print('Input file is: ', inputfile)

    # Run report on file
    EnsembleFileReader().process(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])

