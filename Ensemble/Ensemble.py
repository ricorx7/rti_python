
from PyCRC.CRCCCITT import CRCCCITT


class Ensemble():
    """
    RoweTech Binary Ensemble.
    RTB format.

    """

    # Ensemble header size in bytes
    HeaderSize = 32

    # Checksum size
    ChecksumSize = 4

    def ensembleSize(self, payloadSize):
        return Ensemble.HeaderSize + payloadSize + Ensemble.ChecksumSize

    def calcChecksum(data):
        """
        Calculate the checksum of the ensemble.
        Using CRC-CCITT calculation.
        :param data: Raw ensemble data.
        :return: Checksum value of the ensemble.
        """
        return CRCCCITT.calculate(data)