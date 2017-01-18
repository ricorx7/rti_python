import os.path
import sys
import getopt
import threading
import socket
from Codecs.AdcpCodec import AdcpCodec
from log import logger


class EnsembleFileReader:

    def __init__(self):
        self.codec = None
        self.ens_reader = None
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP Socket
        self.socket.bind(('', 55057))

    def process(self, file_path):
        """
        Read the file and start a thread to monitor the incoming ensembles.
        :param file_path: File  path the read files
        :return:
        """
        # Start thread to monitor incoming ensembles
        # Connect to ensemble server
        self.ens_reader = threading.Thread(name='EnsFileReader', target=self.process_ensembles).start()

        self.codec = AdcpCodec()

        # Process the file
        self.process_file(file_path)

        logger.debug("Completed File reader")

    def process_file(self, file_path):
        """
        Process the file given.  This read from the file
        and add it to the codec.  The codec will then decode
        the data and pass it to the UDP port.
        """
        # Check if the file exist
        if os.path.exists(file_path):

            logger.debug("Open file: " + file_path)

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

    def process_ensembles(self):
        logger.debug("Prepared to receive UDP data.")
        print("Prepared to receive UDP data.")
        while True:
            recv_data, addr = self.socket.recvfrom(4096)
            logger.debug(".")
            print(".")


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

