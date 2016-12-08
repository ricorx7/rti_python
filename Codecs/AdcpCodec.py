

class AdcpCodec():
    """
    ADCP Codec will decode the 
    ADCP data.
    """

    def __init__(self):
        self.BinaryCodec = BinaryCodec()

    def Add(self, data):
        