

class AdcpCodec():
    """
    ADCP Codec will decode the 
    ADCP data.
    """

    def __init__(self):
        self.BinaryCodec = BinaryCodec(55057)

    def Add(self, data):
        