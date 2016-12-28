import logging

from Codecs.BinaryCodec import BinaryCodec
from Codecs.WaveForceCodec import WaveForceCodec

logger = logging.getLogger("ADCP Codec")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

class AdcpCodec:
    """
    ADCP Codec will decode the 
    ADCP data.  There are more than one ADCP format, this will use all the different
    codecs to decode the data.
    """

    def __init__(self, udp_port):
        self.binary_codec = BinaryCodec(udp_port)

        self.WaveForceCodec = WaveForceCodec()
        self.IsWfcEnabled = False

    def add(self, data):
        """
        Add the data to the codecs.
        :param data: Raw data to add to the codecs.
        """
        self.binary_codec.add(data)

    def enable_waveforce_codec(self):
        """
        Enable the WaveForce codec.  This data will be encoded
        into the Matlab format.
        """
        self.IsWfcEnabled = True
        self.binary_codec.EnsembleEvent += self.process_ensemble

    def process_ensemble(self, sender, ens):
        """
        If the WaveForce codec is enabled, then process the ensemble data.
        :param ens: Ensemble data.
        """
        logger.debug("Received processed ensemble")
        if self.IsWfcEnabled:
            logger.debug("Send to WaveForce Codec")
            self.WaveForceCodec.process(ens)
