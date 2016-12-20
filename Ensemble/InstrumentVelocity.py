import json
from Ensemble.Ensemble import Ensemble


class InstrumentVelocity:
    """
    Instrument Velocity DataSet.
    [Bin x Beam] data.
    """

    def __init__(self, num_elements, element_multipiler):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multipiler = element_multipiler
        self.image = 0
        self.name_len = 8
        self.name = "E000002"
        self.Velocities = []
        # Create enough entries for all the (bins x beams)
        # Initialize with bad values
        for bins in range(num_elements):
            bins = []
            for beams in range(element_multipiler):
                bins.append([Ensemble().BadVelocity])

            self.Velocities.append(bins)

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the velocities.
        :param data: Bytearray for the dataset.
        """
        packetpointer = Ensemble.GetBaseDataSize(self.name_len)

        for bin in range(self.num_elements):
            for beam in range(self.element_multipiler):
                self.Velocities[bin][beam] = Ensemble.GetFloat(packetpointer, Ensemble().BytesInFloat, data)
                packetpointer += Ensemble().BytesInFloat

        print(self.Velocities)

    def toJSON(self, pretty=False):
        """
        Convert to JSON.
        :return: JSON string with indents.
        """
        if pretty is True:
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        else:
            return json.dumps(self, default=lambda o: o.__dict__)