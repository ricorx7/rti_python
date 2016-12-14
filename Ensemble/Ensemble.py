
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

    def ones_complement(self, val):
        """
        Calclaute the 1's compliment of a number.
        :param val: Values to calculate.
        :return: 1's compliment of value.
        """
        mask = (1 << val.bit_length()) - 1
        return int(hex(val ^ mask), 16)