import logging

from Utilities.EnsembleReceiver import EnsembleReceiver

logger = logging.getLogger("ADCP")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

class ADCP(EnsembleReceiver):
    """
    Create an ADCP connection.
    """

    def __init__(self):
        """
        Call the super class.
        """
        #super(LivePlot, self).__init__(udp_port)
        super().__init__()

        self.Amplitude = None
        self.BeamVelocity = None
        self.InstrumentVelocity = None
        self.EarthVelocity = None
        self.Correlation = None
        self.BottomTrack = None
        self.EnsembleData = None
        self.AncillaryData = None


    #def close(self):
    #    super.close()

    def process(self, jsonData):
        """
        Process the JSON data that contains the ADCP data.
        :param jsonData: JSON ADCP data.
        :return:
        """
        #logger.info(jsonData["Name"])

        # Beam Velocity
        if "E000001" in jsonData["Name"]:
            self.BeamVelocity = jsonData

        # Instrument Velocity
        if "E000002" in jsonData["Name"]:
            self.InstrumentVelocity = jsonData

        # Earth Velocity
        if "E000003" in jsonData["Name"]:
            self.EarthVelocity = jsonData

        # Amplitude
        if "E000004" in jsonData["Name"]:
            self.Amplitude = jsonData

        # Correlation
        if "E000005" in jsonData["Name"]:
            self.Correlation = jsonData

        # Ensemble Data
        if "E000008" in jsonData["Name"]:
            self.EnsembleData = jsonData

        # Ancillary Data
        if "E000009" in jsonData["Name"]:
            self.AncillaryData = jsonData

        # Bottom Track
        if "E000010" in jsonData["Name"]:
            self.BottomTrack = jsonData

