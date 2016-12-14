import struct
import os.path
import sys
import getopt
from Ensemble.Ensemble import Ensemble

from PyCRC.CRCCCITT import CRCCCITT

class EnsembleFileReport():
    """
    Decode RoweTech ADCP Binary data.
    """

    def __init__(self):
        print("codec")

        self.NumEnsembles = 0
        self.FirstEnsembleNum = 0
        self.LastEnsembleNum = 0

        self.NumBadEnsNum = 0
        self.NumBadPayloadSize = 0
        self.NumBadChecksum = 0
        self.NumBadEnsembles = 0




    def Report(self, infile):
        """
        Read a Rowe DVL/ADCP ensemble file (.ENS)
        """
        # Check if file exist
        if not os.path.isfile(infile):
            print("File path does not exist: ", infile)
            sys.exit()

        with open(infile, 'rb') as f:
            raw = f.read()  # reads entire file. There's probably a smarter option.
            delimiter = '\x80' * 16  # look for first 16 bytes of header
            ensembles = raw.split(delimiter)

            self.NumEnsembles = len(ensembles)

            # Decode all the ensembles and generate a report about the data
            for ensemble_number, ensemble in enumerate(ensembles):
                self.decodeEnsemble(ensemble)

            print("Number of Ensembles: ", self.NumEnsembles)
            print("First Ensemble Number: ", self.FirstEnsembleNum)
            print("Last Ensemble Number: ", self.LastEnsembleNum)
            print("----------------------------------------")
            print("Number of Bad Ensembles: ", self.NumBadEnsembles)
            print("Number of Bad Payload Sizes: ", self.NumBadPayloadSize)
            print("Number of Bad Checksum: ", self.NumBadChecksum)
            print("Number of Bad Ensembles: ", self.NumBadEnsembles)


    def decodeEnsemble(self, ens):

        # Check Ensemble number
        ens_num = struct.unpack("I", ens[16:20])
        ens_num_inv = struct.unpack("I", ens[20:24])
        ens_num_1scomp = Ensemble().ones_complement(ens_num_inv[0])
        #print(self.ones_complement(ens_num_inv[0]))
        #print(ens_num[0])
        if ens_num[0] != ens_num_1scomp:
            self.NumBadEnsembles += 1

        # Check ensemble size
        payload_size = struct.unpack("I", ens[24:28])
        payload_size_inv = struct.unpack("I", ens[28:32])
        payload_size_1scomp = Ensemble().ones_complement(payload_size_inv[0])
        #print(payloadSize[0])
        #print(self.ones_complement(payload_size_inv[0]))
        if payload_size[0] != payload_size_1scomp:
            self.NumBadPayloadSize += 1

        # Set first and last ensemble number
        if self.FirstEnsembleNum == 0:
            self.FirstEnsembleNum = ens_num[0]
        self.LastEnsembleNum = ens_num[0]


        # Ensure the entire ensemble is in the buffer
        if len(ens) >= Ensemble().HeaderSize + payload_size[0] + Ensemble().ChecksumSize:
            # Check checksum
            checksumLoc = Ensemble().HeaderSize + payload_size[0]
            checksum = struct.unpack("I", ens[checksumLoc:checksumLoc + Ensemble().ChecksumSize])

            # Calculate Checksum
            # Use only the payload for the checksum
            ens_payload = ens[Ensemble().HeaderSize:Ensemble().HeaderSize + payload_size[0]]
            calcChecksum = CRCCCITT().calculate(input_data=bytes(ens_payload))
            #print("Calc Checksum: ", calcChecksum)
            #print("Checksum: ", checksum[0])
            #print("Checksum good: ", calcChecksum == checksum[0])

            if checksum[0] != calcChecksum:
                self.NumBadChecksum += 1


def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print('EnsembleFileReport.py -i <inputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('EnsembleFileReport.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
   print('Input file is: ', inputfile)

   # Run report on file
   EnsembleFileReport().Report(inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])




