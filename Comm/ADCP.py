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



    def close(self):
        super.close()

    def process(self, jsonData):
        """
        Process the JSON data that contains the ADCP data.
        :param jsonData: JSON ADCP data.
        :return:
        """
        #logger.info(jsonData["Name"])
        if "E000004" in jsonData["Name"]:
            logger.info(jsonData["Name"])
            self.Amplitude = jsonData
