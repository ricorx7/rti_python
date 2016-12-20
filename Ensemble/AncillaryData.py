import json
import struct
from Ensemble.Ensemble import Ensemble


class AncillaryData:
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
        self.name = "E000009"

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
        the velocities.
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


        print(self.FirstBinRange)
        print(self.BinSize)
        print(self.Heading)
        print(self.Pitch)
        print(self.Roll)
        print(self.Salinity)
        print(self.SpeedOfSound)


    def toJSON(self, pretty=False):
        """
        Convert to JSON.
        :return: JSON string with indents.
        """
        if pretty is True:
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        else:
            return json.dumps(self, default=lambda o: o.__dict__)


