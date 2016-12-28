import logging

logger = logging.getLogger("WaveForce Codec")
logger.setLevel(logging.ERROR)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

class WaveForceCodec:
    """
    Decode the ensemble data into a WaveForce Matlab file format.
    """

    def __init__(self):
        self.Txt = ""
        self.Lat = 0.0
        self.Lon = 0.0

    def process(self, ens):
        """
        Process the ensemble data.
        :param ens: Ensemble data.
        :return:
        """
        self.process_txt(ens)
        self.process_lat(ens)
        self.process_lon(ens)

    def process_txt(self, ens):
        """
        This will give a text description of the burst.  This will include the record number,
        the serial number and the date and time of the burst started.

        Data Type: Text
        Rows: 1
        Columns: Text Length
        txt = 2013/07/30 21:00:00.00, Record No. 7, SN013B0000000000000000000000000000
        :param ens: Ensemble data.
        """
        self.Txt = ""

    def process_lat(self, ens):
        """
        The latitude location where the burst was collected.

        Data Type: Double
        Rows: 1
        Columns: 1
        lat = 32.865
        :param ens: Ensemble data.
        """
        self.Lat = 0.0

    def process_lon(self, ens):
        """
        The longitude location where the burst was collected.

        Data Type: Double
        Rows: 1
        Columns: 1
        lon = -117.26
        :param ens: Ensemble data.
        """
        self.Lon = 0.0
