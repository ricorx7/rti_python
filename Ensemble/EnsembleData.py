import struct
import logging
from Ensemble.Ensemble import Ensemble

logger = logging.getLogger("Ensemble Data")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class EnsembleData:
    """
    Ensemble Data DataSet.
    Integer values that give details about the ensemble.
    """

    def __init__(self, num_elements, element_multiplier):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multiplier = element_multiplier
        self.image = 0
        self.name_len = 8
        self.Name = "E000008"

        self.EnsembleNumber = 0
        self.NumBins = 0
        self.NumBeams = 0
        self.DesiredPingCount = 0
        self.ActualPingCount = 0
        self.SerialNumber = ""
        self.SysFirmwareMajor = ""
        self.SysFirmwareMinor = ""
        self.SysFirmwareRevision = ""
        self.SysFirmwareSubsystemCode = ""
        self.SubsystemConfig = ""
        self.Status = 0
        self.Year = 0
        self.Month = 0
        self.Day = 0
        self.Hour = 0
        self.Minute = 0
        self.Second = 0
        self.HSec = 0

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the velocities.
        :param data: Bytearray for the dataset.
        """
        packet_pointer = Ensemble.GetBaseDataSize(self.name_len)

        self.EnsembleNumber = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 0, Ensemble().BytesInInt32, data)
        self.NumBins = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 1, Ensemble().BytesInInt32, data)
        self.NumBeams = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 2, Ensemble().BytesInInt32, data)
        self.DesiredPingCount = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 3, Ensemble().BytesInInt32, data)
        self.ActualPingCount = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 4, Ensemble().BytesInInt32, data)
        self.Status = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 5, Ensemble().BytesInInt32, data)
        self.Year = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 6, Ensemble().BytesInInt32, data)
        self.Month = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 7, Ensemble().BytesInInt32, data)
        self.Day = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 8, Ensemble().BytesInInt32, data)
        self.Hour = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 9, Ensemble().BytesInInt32, data)
        self.Minute = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 10, Ensemble().BytesInInt32, data)
        self.Second = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 11, Ensemble().BytesInInt32, data)
        self.HSec = Ensemble.GetInt32(packet_pointer + Ensemble().BytesInInt32 * 12, Ensemble().BytesInInt32, data)

        self.SerialNumber = str(data[packet_pointer+Ensemble().BytesInInt32*13:packet_pointer+Ensemble().BytesInInt32*21], "UTF-8")
        self.SysFirmwareRevision = struct.unpack("B", data[packet_pointer+Ensemble().BytesInInt32*21 + 0:packet_pointer+Ensemble().BytesInInt32*21 + 1])[0]
        self.SysFirmwareMinor = struct.unpack("B", data[packet_pointer+Ensemble().BytesInInt32*21 + 1:packet_pointer+Ensemble().BytesInInt32*21 + 2])[0]
        self.SysFirmwareMajor = struct.unpack("B", data[packet_pointer + Ensemble().BytesInInt32 * 21 + 2:packet_pointer + Ensemble().BytesInInt32 * 21 + 3])[0]
        self.SysFirmwareSubsystemCode = str(data[packet_pointer + Ensemble().BytesInInt32 * 21 + 3:packet_pointer + Ensemble().BytesInInt32 * 21 + 4], "UTF-8")

        self.SubsystemConfig = struct.unpack("B", data[packet_pointer + Ensemble().BytesInInt32 * 22 + 3:packet_pointer + Ensemble().BytesInInt32 * 22 + 4])[0]

        logger.debug(self.EnsembleNumber)
        logger.debug(str(self.Month) + "/" + str(self.Day) + "/" + str(self.Year) + "  " + str(self.Hour) + ":" + str(self.Minute) + ":" + str(self.Second) + "." + str(self.HSec))
        logger.debug(self.SerialNumber)
        logger.debug(str(self.SysFirmwareMajor) + "." + str(self.SysFirmwareMinor) + "." + str(self.SysFirmwareRevision) + "-" + str(self.SysFirmwareSubsystemCode))
        logger.debug(self.SubsystemConfig)



