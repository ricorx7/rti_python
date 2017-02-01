from rti_python.Ensemble.Ensemble import Ensemble
from rti_python.log import logger


class Amplitude:
    """
    Amplitude DataSet.
    [Bin x Beam] data.
    """

    def __init__(self, num_elements, element_multiplier):
        self.ds_type = 10
        self.num_elements = num_elements
        self.element_multiplier = element_multiplier
        self.image = 0
        self.name_len = 8
        self.Name = "E000004"
        self.Amplitude = []

        #self.EnsembleNumber = ensemble_number
        #self.SerialNumber = serial_number
        #self.DateTime = date_time

        # Create enough entries for all the (bins x beams)
        # Initialize with bad values
        for bins in range(num_elements):
            bins = []
            for beams in range(element_multiplier):
                bins.append([Ensemble().BadVelocity])

            self.Amplitude.append(bins)

    def decode(self, data):
        """
        Take the data bytearray.  Decode the data to populate
        the velocities.
        :param data: Bytearray for the dataset.
        """
        packet_pointer = Ensemble.GetBaseDataSize(self.name_len)

        for bin in range(self.num_elements):
            for beam in range(self.element_multiplier):
                self.Amplitude[bin][beam] = Ensemble.GetFloat(packet_pointer, Ensemble().BytesInFloat, data)
                packet_pointer += Ensemble().BytesInFloat

        logger.debug(self.Amplitude)
