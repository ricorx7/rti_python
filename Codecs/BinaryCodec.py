import struct

from Ensemble.Ensemble import Ensemble

from PyCRC.CRCCCITT import CRCCCITT

class BinaryCodec():
    """
    Decode RoweTech ADCP Binary data.
    """

    def __init__(self):
        print("codec")
        self.buffer = bytearray()

    def add(self, data):

        # Add to buffer and Decode
        self.buffer.extend(data)

        self.findEnsemble()

    def findEnsemble(self):

        delimiter = b'\x80'*16 # look for first 16 bytes of header
        ensStart = self.buffer.find(delimiter)

        #print("EnsStart: ", ensStart)
        #print("Buffer Size: ", len(self.buffer))

        if ensStart >= 0 and len(self.buffer) > 32 + ensStart:
            #Decode the Ensemble
            self.decodeEnsemble(ensStart)

    def decodeEnsemble(self, ensStart):

        # Check Ensemble number
        ensNum = struct.unpack("I", self.buffer[ensStart+16:ensStart+20])
        ensNumInv = struct.unpack("I", self.buffer[ensStart+20:ensStart+24])
        print(ensNum[0])
        print(self.ones_complement(ensNumInv[0]))


        # Check ensemble size
        payloadSize = struct.unpack("I", self.buffer[ensStart+24:ensStart+28])
        payloadSizeInv = struct.unpack("I", self.buffer[ensStart+28:ensStart+32])
        print(payloadSize[0])
        print(self.ones_complement(payloadSizeInv[0]))

        # Ensure the entire ensemble is in the buffer
        if len(self.buffer) >= ensStart + Ensemble().HeaderSize + payloadSize[0] + Ensemble().ChecksumSize:
            # Check checksum
            checksumLoc = ensStart + Ensemble().HeaderSize + payloadSize[0]
            checksum = struct.unpack("I", self.buffer[checksumLoc:checksumLoc + Ensemble().ChecksumSize])

            # Calculate Checksum
            ens = self.buffer[ensStart + Ensemble().HeaderSize:ensStart + Ensemble().ChecksumSize + payloadSize[0]]
            calcChecksum = CRCCCITT().calculate(input_data=bytes(ens))
            print("Calc Checksum: ", calcChecksum)
            print("Checksum: ", checksum[0])

            #print(checksum)
            #print(calcChecksum)

            # Decode data

            # Stream data

            # Remove ensemble from buffer
            ensEnd = ensStart + Ensemble().HeaderSize + payloadSize[0] + Ensemble().ChecksumSize
            del self.buffer[0:ensEnd]

    def ones_complement(self, val):
        mask = (1 << val.bit_length()) - 1
        return int(hex(val ^ mask), 16)

    def twos_complement(self, val, nbits):
        """compute the 2's compliment of int value val"""
        if (val & (1 << (nbits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << nbits)  # compute negative value
        return val
