import struct


class Ensemble():
    """
    RoweTech Binary Ensemble.
    RTB format.

    """

    # Ensemble header size in bytes
    HeaderSize = 32

    # Checksum size
    ChecksumSize = 4

    # Maximum number of datasets.
    MaxNumDataSets = 20

    # Number of bytes in Int32
    BytesInInt32 = 4

    # Number of bytes in Float
    BytesInFloat = 4

    # Number of elements in dataset header
    NUM_DATASET_HEADER_ELEMENTS = 6

    # Bad Velocity
    BadVelocity = 88.888

    def __init__(self):
        self.IsBeamVelocity = False
        self.BeamVelocity = None

    def AddBeamVelocity(self, beamVel):
        """
        Add a Beam Velocity object to the ensemble.
        Set the flag that the dataset is added.
        :param beamVel: Beam Velocity object.
        """
        self.BeamVelocity = True
        self.BeamVelocity = beamVel

    @staticmethod
    def GetInt32(start, numBytes, ens):
        """
        Convert the bytes given into an int32.
        This will look in the ens given.
        :param start: Start location.
        :param numBytes: Number of bytes in the int32.
        :param ens: Buffer containing the bytearray data.
        :return: Int32 of the data in the buffer.
        """
        return struct.unpack("I", ens[start:start + numBytes])

    @staticmethod
    def GetFloat(start, numBytes, ens):
        """
        Convert the bytes given into an int32.
        This will look in the ens given.
        :param start: Start location.
        :param numBytes: Number of bytes in the int32.
        :param ens: Buffer containing the bytearray data.
        :return: Int32 of the data in the buffer.
        """
        return struct.unpack("f", ens[start:start + numBytes])

    @staticmethod
    def GetDataSetSize(ds_type, name_len, num_elements, element_multipler):
        """
        Get the dataset size.
        :param ds_type: Dataset type. (Int, float, ...)
        :param name_len: Length of the name.
        :param num_elements: Number of elements.
        :param element_multipler: Element mulitpiler.
        :return: Size of the dataset in bytes.
        """

        # Number of bytes in the data type
        datatype_size = 4
        if ds_type is 50:      # Byte Datatype
            datatype_size = 1
        elif ds_type is 20:    # Int Datatype
            datatype_size = 4
        elif ds_type is 10:    # Float Datatype
            datatype_size = 4

        return ((num_elements * element_multipler) * datatype_size) + Ensemble.GetBaseDataSize(name_len)

    @staticmethod
    def GetBaseDataSize(name_len):
        """
        Get the size of the header for a dataset.
        :param name_len: Length of the name.
        :return: Dataset header size in bytes.
        """
        return name_len + (Ensemble().BytesInInt32 * (Ensemble().NUM_DATASET_HEADER_ELEMENTS-1))

    @staticmethod
    def ensembleSize(payloadSize):
        return Ensemble.HeaderSize + payloadSize + Ensemble.ChecksumSize

    @staticmethod
    def ones_complement(self, val):
        """
        Calclaute the 1's compliment of a number.
        :param val: Values to calculate.
        :return: 1's compliment of value.
        """
        mask = (1 << val.bit_length()) - 1
        return int(hex(val ^ mask), 16)