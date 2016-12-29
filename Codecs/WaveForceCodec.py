import logging
import struct
import threading

logger = logging.getLogger("WaveForce Codec")
logger.setLevel(logging.ERROR)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)

class WaveForceCodec:
    """
    Decode the ensemble data into a WaveForce Matlab file format.
    """

    def __init__(self):
        #self.Txt = ""
        self.Lat = 0.0
        self.Lon = 0.0
        self.EnsInBurst = 0
        self.FilePath = ""
        self.EnsInBurst = 0
        self.Buffer = []
        self.BufferCount = 0
        self.RecordCount = 0
        self.Bin1 = 0
        self.Bin2 = 0
        self.Bin3 = 0

    def init(self, ens_in_burst, path, lat, lon, bin1, bin2, bin3):
        """
        Initialize the wave recorder
        :param ens_in_burst: Number of ensembles in a burst.
        :param path: File path to store the file.
        :param lat: Latitude data.
        :param lon: Longitude data.
        :param bin1: First selected bin.
        :param bin2: Second selected bin.
        :param bin3: Third selected bin.
        """
        self.EnsInBurst = ens_in_burst
        self.FilePath = path
        self.Lat = lat
        self.Lon = lon
        self.Buffer = []
        self.BufferCount = 0
        self.Bin1 = bin1
        self.Bin2 = bin2
        self.Bin3 = bin3
        self.RecordCount = 0

    def add(self, ens):
        """
        Add the ensemble to the buffer.  When the buffer number has been met,
        process the buffer and output the data to a matlab file.
        :param ens: Ensemble to buffer.
        """
        if self.EnsInBurst > 0:
            logger.debug("Added Ensemble to burst")

            # Add to the buffer
            self.Buffer.append(ens)
            self.BufferCount += 1

            # Process the buffer when a burst is complete
            if self.BufferCount == self.EnsInBurst:
                # Get the ensembles from the buffer
                ens_buff = self.Buffer[0:self.EnsInBurst]

                # Remove the ensembles from the buffer
                del self.Buffer[0:self.EnsInBurst]
                self.BufferCount = 0

                # Process the buffer
                #self.process(ens_buff)
                th = threading.Thread(target=self.process, args=[ens_buff])
                th.start()

    def process(self, ens_buff):
        """
        Process all the data in the ensemble buffer.
        :param ens_buff: Ensemble data buffer.
        """
        logger.debug("Process Waves Burst")

        ba = bytearray()

        ba.extend(self.process_txt(ens_buff[0]))
        ba.extend(self.process_lat(ens_buff[0]))
        ba.extend(self.process_lon(ens_buff[0]))

        # Write the file
        self.write_file(ba)

        # Increment the record count
        self.RecordCount += 1

    def write_file(self, ba):
        """
        Write the Bytearray to a file.  Save it with the record number
        :param ba: Byte Array with record data.
        :return:
        """
        filename = self.FilePath + "D0000" + str(self.RecordCount) + ".mat"
        with open(filename, 'wb') as f:
            f.write(ba)

    def process_txt(self, ens):
        """
        This will give a text description of the burst.  This will include the record number,
        the serial number and the date and time of the burst started.

        Data Type: Text
        Rows: 1
        Columns: Text Length
        txt = 2013/07/30 21:00:00.00, Record No. 7, SN013B0000000000000000000000000000
        :param ens: Ensemble data.
        :return: Byte array of the data in MATLAB format.
        """
        txt = ens.EnsembleData.datetime_str() + ", "
        txt += "Record No. " + str(self.RecordCount) + ", "
        txt += "SN" + ens.EnsembleData.SerialNumber

        ba = bytearray()
        ba.extend(struct.pack('i', 11))         # Indicate string
        ba.extend(struct.pack('i', 1))          # Rows - 1 per record
        ba.extend(struct.pack("i", len(txt)))   # Columns - Length of the txt
        ba.extend(struct.pack("i", 0))          # Imaginary, if 1, then the matrix has an imaginary part
        ba.extend(struct.pack("i", 4))          # Name Length

        for code in map(ord, 'txt '):           # Name
            ba.extend([code])

        for code in map(ord, txt):              # Txt Value
            ba.extend([code])



        return ba

    def process_lat(self, ens):
        """
        The latitude location where the burst was collected.

        Data Type: Double
        Rows: 1
        Columns: 1
        lat = 32.865
        :param ens: Ensemble data.
        """
        lat = 0.0
        if ens.IsWavesInfo:
            lat = ens.WavesInfo.Lat
        else:
            lat = self.Lat

        ba = bytearray()
        ba.extend(struct.pack('i', 0))      # Indicate double
        ba.extend(struct.pack('i', 1))      # Rows - 1 per record
        ba.extend(struct.pack("i", 1))      # Columns - 1 per record
        ba.extend(struct.pack("i", 0))      # Imaginary, if 1, then the matrix has an imaginary part
        ba.extend(struct.pack("i", 4))      # Name Length

        for code in map(ord, 'lat '):       # Name
            ba.extend([code])

        ba.extend(struct.pack("d", lat))    # Lat Value

        return ba

    def process_lon(self, ens):
        """
        The longitude location where the burst was collected.

        Data Type: Double
        Rows: 1
        Columns: 1
        lon = -117.26
        :param ens: Ensemble data.
        """
        lon = 0.0
        if ens.IsWavesInfo:
            lon = ens.WavesInfo.Lat
        else:
            lon = self.Lon

        ba = bytearray()
        ba.extend(struct.pack('i', 0))      # Indicate double
        ba.extend(struct.pack('i', 1))      # Rows - 1 per record
        ba.extend(struct.pack("i", 1))      # Columns - 1 per record
        ba.extend(struct.pack("i", 0))      # Imaginary
        ba.extend(struct.pack("i", 4))      # Name Length

        for code in map(ord, 'lon '):       # Name
            ba.extend([code])

        ba.extend(struct.pack("d", lon))    # Lon Value

        return ba
