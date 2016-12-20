import json
from Ensemble.Ensemble import Ensemble


class GoodBeam:
    """
    Good Beam DataSet.
    Indicate if the beam data is good.
    [Bin x Beam] data.
    """

    def __init__(self, num_elements, element_multiplier):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multiplier = element_multiplier
        self.image = 0
        self.name_len = 8
        self.name = "E000006"
        self.GoodBeam = []
        # Create enough entries for all the (bins x beams)
        # Initialize with bad values
        for bins in range(num_elements):
            bins = []
            for beams in range(element_multiplier):
                bins.append([0])

            self.GoodBeam.append(bins)

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the velocities.
        :param data: Bytearray for the dataset.
        """
        packet_pointer = Ensemble.GetBaseDataSize(self.name_len)

        for bin in range(self.num_elements):
            for beam in range(self.element_multiplier):
                self.GoodBeam[bin][beam] = Ensemble.GetInt32(packet_pointer, Ensemble().BytesInInt32, data)
                packet_pointer += Ensemble().BytesInInt32

        print(self.GoodBeam)

    def toJSON(self, pretty=False):
        """
        Convert to JSON.
        :return: JSON string with indents.
        """
        if pretty is True:
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        else:
            return json.dumps(self, default=lambda o: o.__dict__)