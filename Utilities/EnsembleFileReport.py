import struct
import logging
import os.path
import sys
import getopt
from Ensemble.Ensemble import Ensemble

from PyCRC.CRCCCITT import CRCCCITT


logger = logging.getLogger("Ensemble File Report")
logger.setLevel(logging.ERROR)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

class EnsembleFileReport:
    """
    Decode RoweTech ADCP Binary data.
    """

    def __init__(self, verbose=False):
        print("codec")

        self.NumEnsembles = 0
        self.FirstEnsembleNum = 0
        self.LastEnsembleNum = 0

        self.NumGoodEnsembles = 0

        self.NumBadEnsNum = 0
        self.NumBadPayloadSize = 0
        self.NumBadChecksum = 0
        self.NumBadEnsembles = 0
        self.NumIncompleteEnsembles = 0
        self.ContainsMultipleRuns = False

        self.HeadersFound = 0

        self.prevEnsNum = 0

        self.verbose = verbose

    def report(self, infile):
        """
        Read a Rowe DVL/ADCP ensemble file (.ENS)
        """
        # Check if file exist
        if not os.path.isfile(infile):
            print("File path does not exist: ", infile)
            sys.exit()

        with open(infile, 'rb') as f:
            # Read entire file.
            raw = f.read()

            ens_start_list = list()
            ens_list = list()

            # look for first 16 bytes of header
            delimiter = b'\x80' * 16

            # Added file to byte array
            raw_ba = bytearray()
            raw_ba.extend(raw)

            # Look for the first ensemble
            ens_found = raw_ba.find(delimiter)

            # Process the found ensemble
            while ens_found >= 0:

                # Count number of headers found
                self.HeadersFound += 1

                # Add the ensemble found to the list
                ens_start_list.append(ens_found)

                if len(ens_start_list) > 0:
                    # Create byte array to hold ensemble
                    # Ensemble lost its header, so add it back in
                    # Add ensemble to the list
                    ens_ba = bytearray()
                    ens_ba.extend(delimiter)
                    prev_ens_found = ens_start_list[len(ens_list)-1]
                    ens_ba.extend(raw_ba[prev_ens_found:ens_found])
                    ens_list.append(ens_ba)

                # Remove ensemble header to find the next
                del raw_ba[ens_found:ens_found+16]

                # Find the next ensemble
                ens_found = raw_ba.find(delimiter)

            # Decode all the ensembles found and generate a report about the data
            for index in range(len(ens_list)):
                self.decode_ensemble(ens_list[index])

            print("----------------------------------------")
            print("Number of Ensembles: ", self.NumEnsembles)
            print("First Ensemble Number: ", self.FirstEnsembleNum)
            print("Last Ensemble Number: ", self.LastEnsembleNum)
            print("Number of Good Ensembles: ", self.NumGoodEnsembles)
            print("----------------------------------------")
            print("Number of Bad Ensemble Numbers: ", self.NumBadEnsNum)
            print("Number of Bad Payload Sizes: ", self.NumBadPayloadSize)
            print("Number of Bad Checksum: ", self.NumBadChecksum)
            print("Number of Bad Ensembles: ", self.NumBadEnsembles)
            print("Number of Incomplete Ensembles: ", self.NumIncompleteEnsembles)
            if self.ContainsMultipleRuns:
                print("* File contains multiple runs, ensemble numbers restarted")

            print("----------------------------------------")
            print("Number of Headers Found: ", self.HeadersFound)

    def decode_ensemble(self, ens):
        """
        Decode the ensemble.
        :param ens: Ensemble byte array.
        """
        self.NumEnsembles += 1

        # Ensure enough data is present to check the header
        if len(ens) < Ensemble().HeaderSize:
            self.NumIncompleteEnsembles += 1
            return

        # Check Ensemble number
        ens_num = struct.unpack("I", ens[16:20])
        ens_num_inv = struct.unpack("I", ens[20:24])
        logger.debug("Ensemble Number: " + str(ens_num[0]))
        logger.debug("Ensemble Number 1sComp: " + str(ens_num_inv[0]))

        if len(ens_num_inv) != 0:
            ens_num_1s_comp = Ensemble.ones_complement(ens_num_inv[0])

            if ens_num[0] != ens_num_1s_comp:
                self.NumBadEnsNum += 1
        else:
            self.NumBadEnsNum += 1

        if self.prevEnsNum != 0 and ens_num[0] != self.prevEnsNum+1:
            self.ContainsMultipleRuns = True
            print("Cur ENS Num: " + str(ens_num[0]))
            print("Prev ENS Num: " + str(self.prevEnsNum))

        self.prevEnsNum = ens_num[0]

        # Check ensemble size
        payload_size = struct.unpack("I", ens[24:28])
        payload_size_inv = struct.unpack("I", ens[28:32])
        payload_size_1s_comp = Ensemble.ones_complement(payload_size_inv[0])

        if payload_size[0] != payload_size_1s_comp:
            self.NumBadPayloadSize += 1

        # Set first and last ensemble number
        if self.FirstEnsembleNum == 0:
            self.FirstEnsembleNum = ens_num[0]

        self.LastEnsembleNum = ens_num[0]

        self.printVerbose("EnsNum: " + str(ens_num[0]) + " : " + str(ens_num_1s_comp))
        self.printVerbose("Payload Size: " + str(payload_size[0]) + " : " + str(payload_size_1s_comp))

        # Ensure the entire ensemble is in the buffer
        if len(ens) >= Ensemble().HeaderSize + payload_size[0] + Ensemble().ChecksumSize:
            # Get checksum
            checksumLoc = Ensemble().HeaderSize + payload_size[0]
            checksum = struct.unpack("I", ens[checksumLoc:checksumLoc + Ensemble().ChecksumSize])

            # Calculate Checksum
            # Use only the payload for the checksum
            ens_payload = ens[Ensemble().HeaderSize:Ensemble().HeaderSize + payload_size[0]]
            calcChecksum = CRCCCITT().calculate(input_data=bytes(ens_payload))
            self.printVerbose("Checksum: " + str(checksum[0]) + " : " + str(calcChecksum))

            # Check the checksum
            if checksum[0] != calcChecksum:
                self.NumBadChecksum += 1
            else:
                self.NumGoodEnsembles += 1
        else:
            # Not a complete ensemble
            self.NumIncompleteEnsembles += 1

    def printVerbose(self, msg):
        """
        Print the message if verbose is turned on.
        :param msg: Message to print.
        :return:
        """
        if self.verbose:
            print(msg)


def main(argv):
    inputfile = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv,"hvi:",["ifile=","verbose"])
    except getopt.GetoptError:
        print('EnsembleFileReport.py -i <inputfile> -v')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('EnsembleFileReport.py -i <inputfile> -v')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
            print("Verbose ON")
    print('Input file is: ', inputfile)

    # Run report on file
    EnsembleFileReport(verbose).report(inputfile)

if __name__ == "__main__":
    main(sys.argv[1:])




