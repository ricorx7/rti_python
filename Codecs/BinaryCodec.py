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

        if ensStart >= 0 and len(self.buffer) > Ensemble().HeaderSize + ensStart:
            #Decode the Ensemble
            self.decodeEnsemble(ensStart)

    def decodeEnsemble(self, ensStart):

        # Check Ensemble number
        ensNum = struct.unpack("I", self.buffer[ensStart+16:ensStart+20])
        #print(ensNum[0])
        #ensNumInv = struct.unpack("I", self.buffer[ensStart+20:ensStart+24])
        #print(self.ones_complement(ensNumInv[0]))


        # Check ensemble size
        payloadSize = struct.unpack("I", self.buffer[ensStart+24:ensStart+28])
        #print(payloadSize[0])
        #payloadSizeInv = struct.unpack("I", self.buffer[ensStart+28:ensStart+32])
        #print(self.ones_complement(payloadSizeInv[0]))

        # Ensure the entire ensemble is in the buffer
        if len(self.buffer) >= ensStart + Ensemble().HeaderSize + payloadSize[0] + Ensemble().ChecksumSize:
            # Check checksum
            checksumLoc = ensStart + Ensemble().HeaderSize + payloadSize[0]
            checksum = struct.unpack("I", self.buffer[checksumLoc:checksumLoc + Ensemble().ChecksumSize])

            # Calculate Checksum
            # Use only the payload for the checksum
            ens = self.buffer[ensStart + Ensemble().HeaderSize:ensStart + Ensemble().HeaderSize + payloadSize[0]]
            calcChecksum = CRCCCITT().calculate(input_data=bytes(ens))
            #print("Calc Checksum: ", calcChecksum)
            #print("Checksum: ", checksum[0])
            #print("Checksum good: ", calcChecksum == checksum[0])

            if checksum[0] == calcChecksum:
                print(ensNum[0])
                # Decode data
                self.decodeDataSets(ens)


                # Stream data

            # Remove ensemble from buffer
            ensEnd = ensStart + Ensemble().HeaderSize + payloadSize[0] + Ensemble().ChecksumSize
            del self.buffer[0:ensEnd]

    def decodeDataSets(self, ens):
        print(ens)
        packetPointer = 0
        type = 0
        numElements = 0
        elementMultiplier = 0
        imag = 0
        nameLen = 0
        name = ""
        dataSetSize = 0

        for x in range(Ensemble().MaxNumDataSets):
            type = self.getInt32(packetPointer+(Ensemble.BytesInInt32 * 0), Ensemble().BytesInInt32, ens)
            numElements = self.getInt32(packetPointer+(Ensemble.BytesInInt32 * 1), Ensemble().BytesInInt32, ens)
            elementMultiplier = self.getInt32(packetPointer+(Ensemble.BytesInInt32 * 2), Ensemble().BytesInInt32, ens)
            image = self.getInt32(packetPointer+(Ensemble.BytesInInt32 * 3), Ensemble().BytesInInt32, ens)
            nameLen = self.getInt32(packetPointer+(Ensemble.BytesInInt32 * 4), Ensemble().BytesInInt32, ens)
            name = str(ens[packetPointer+(Ensemble.BytesInInt32 * 5):packetPointer+(Ensemble.BytesInInt32 * 5)+8], 'UTF-8')

            print(type)
            print(numElements)
            print(elementMultiplier)
            print(name)

    def getInt32(self, start, numBytes, ens):
        #print(start)
        #print(numBytes)
        #print(ens[start:start + numBytes])
        return struct.unpack("I", ens[start:start + numBytes])


    def ones_complement(self, val):
        mask = (1 << val.bit_length()) - 1
        return int(hex(val ^ mask), 16)

    def twos_complement(self, val, nbits):
        """compute the 2's compliment of int value val"""
        if (val & (1 << (nbits - 1))) != 0:  # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << nbits)  # compute negative value
        return val
