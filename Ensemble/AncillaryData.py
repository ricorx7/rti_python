import logging
from Ensemble.Ensemble import Ensemble

logger = logging.getLogger("Ancillary Data")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class AncillaryData:
    """
    Ancillary Data DataSet.
    Float values that give details about the ensemble.
    """

    def __init__(self, num_elements, element_multiplier):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multiplier = element_multiplier
        self.image = 0
        self.name_len = 8
        self.Name = "E000009"

        self.FirstBinRange = 0.0
        self.BinSize = 0.0
        self.FirstPingTime = 0.0
        self.LastPingTime = 0.0
        self.Heading = 0.0
        self.Pitch = 0.0
        self.Roll = 0.0
        self.WaterTemp = 0.0
        self.SystemTemp = 0.0
        self.Salinity = 0.0
        self.Pressure = 0.0
        self.TransducerDepth = 0.0
        self.SpeedOfSound = 0.0

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the values.
        :param data: Bytearray for the dataset.
        """
        packet_pointer = Ensemble.GetBaseDataSize(self.name_len)

        self.FirstBinRange = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 0, Ensemble().BytesInFloat, data)
        self.BinSize = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 1, Ensemble().BytesInFloat, data)
        self.FirstPingTime = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 2, Ensemble().BytesInFloat, data)
        self.LastPingTime = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 3, Ensemble().BytesInFloat, data)
        self.Heading = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 4, Ensemble().BytesInFloat, data)
        self.Pitch = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 5, Ensemble().BytesInFloat, data)
        self.Roll = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 6, Ensemble().BytesInFloat, data)
        self.WaterTemp = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 7, Ensemble().BytesInFloat, data)
        self.SystemTemp = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 8, Ensemble().BytesInFloat, data)
        self.Salinity = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 9, Ensemble().BytesInFloat, data)
        self.Pressure = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 10, Ensemble().BytesInFloat, data)
        self.TransducerDepth = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 11, Ensemble().BytesInFloat, data)
        self.SpeedOfSound = Ensemble.GetFloat(packet_pointer + Ensemble().BytesInFloat * 12, Ensemble().BytesInFloat, data)

        logger.debug(self.FirstBinRange)
        logger.debug(self.BinSize)
        logger.debug(self.Heading)
        logger.debug(self.Pitch)
        logger.debug(self.Roll)
        logger.debug(self.Salinity)
        logger.debug(self.SpeedOfSound)



