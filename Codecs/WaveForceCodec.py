import logging
import struct
import threading
from Waves.WaveEnsemble import WaveEnsemble

logger = logging.getLogger("WaveForce Codec")
logger.setLevel(logging.ERROR)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(name)s:%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class WaveForceCodec:
    """
    Decode the ensemble data into a WaveForce Matlab file format.
    """

    def __init__(self):
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
        self.firstTime = 0
        self.secondTime = 0         # Used to calculate the sample timing
        self.selected_bin = []

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

        self.selected_bin.append(bin1)
        self.selected_bin.append(bin2)
        self.selected_bin.append(bin3)

        self.firstTime = 0
        self.secondTime = 0         # Used to calculate the sample timing

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
                th = threading.Thread(target=self.process, args=[ens_buff])
                th.start()

    def process(self, ens_buff):
        """
        Process all the data in the ensemble buffer.
        :param ens_buff: Ensemble data buffer.
        """
        logger.debug("Process Waves Burst")

        ens_waves_buff = []
        # Convert the buffer to wave ensembles
        for ens in ens_buff:
            ens_waves_buff.append(WaveEnsemble().add(ens, self.selected_bin))

        
        ba = bytearray()

        # Get the position time from the first ensemble
        ba.extend(self.process_txt(ens_buff[0]))
        ba.extend(self.process_lat(ens_buff[0]))
        ba.extend(self.process_lon(ens_buff[0]))
        ba.extend(self.process_wft(ens_buff[0]))
        ba.extend(self.process_wdt(ens_buff))

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
        ba.extend(struct.pack('i', 11))         # Indicate float string
        ba.extend(struct.pack('i', 1))          # Rows - 1 per record
        ba.extend(struct.pack("i", len(txt)))   # Columns - Length of the txt
        ba.extend(struct.pack("i", 0))          # Imaginary, if 1, then the matrix has an imaginary part
        ba.extend(struct.pack("i", 4))          # Name Length

        for code in map(ord, 'txt '):           # Name
            ba.extend([code])

        for code in map(ord, txt):              # Txt Value
            ba.extend(struct.pack('f', float(code)))

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

    def process_wft(self, ens):
        """
        First sample time of the burst in seconds. The value is in hours of a day. WFT  * 24 =

        Data Type: Double
        Rows: 1
        Columns: 1
        wft = 7.3545e+05
        :param ens: Ensemble data.
        """
        self.firstTime = self.time_stamp_seconds(ens)

        ba = bytearray()
        ba.extend(struct.pack('i', 0))      # Indicate double
        ba.extend(struct.pack('i', 1))      # Rows - 1 per record
        ba.extend(struct.pack("i", 1))      # Columns - 1 per record
        ba.extend(struct.pack("i", 0))      # Imaginary
        ba.extend(struct.pack("i", 4))      # Name Length

        for code in map(ord, 'wft '):       # Name
            ba.extend([code])

        ba.extend(struct.pack("d", self.firstTime))    # WFT Value

        return ba


    def process_wdt(self, ens_buff):
        """
        Time between each sample.  The time is in seconds.

        Data Type: Double
        Rows: 1
        Columns: 1
        wft = 0.5000
        :param ens: Ensemble data.
        """
        # Find the first and second time
        # Make sure that if we are interleaved,
        # that we take the next sample that is like the original subsystem config

        ba = bytearray()

        if len(ens_buff) >= 4:
            # Get the first 4 Beam sample
            if ens_buff[0].IsEnsembleData:
                subcfg = ens_buff[0].EnsembleData.SubsystemConfig
                subcode =ens_buff[0].EnsembleData.SysFirmwareSubsystemCode
                self.firstTime = self.time_stamp_seconds(ens_buff[0])

                # Check if both subsystems match
                # If they do match, then there is no interleaving and we can take the next sample
                # If there is interleaving, then we have to wait for the next sample, because the first 2 go together
                if ens_buff[1].EnsembleData.SubsystemConfig == subcfg and ens_buff[1].EnsembleData.SysFirmwareSubsystemCode == subcode:
                    self.secondTime = WaveForceCodec.time_stamp_seconds(ens_buff[1])
                else:
                    self.secondTime = WaveForceCodec.time_stamp_seconds(ens_buff[2])

            wdt = self.secondTime - self.firstTime

            ba.extend(struct.pack('i', 0))      # Indicate double
            ba.extend(struct.pack('i', 1))      # Rows - 1 per record
            ba.extend(struct.pack("i", 1))      # Columns - 1 per record
            ba.extend(struct.pack("i", 0))      # Imaginary
            ba.extend(struct.pack("i", 4))      # Name Length

            for code in map(ord, 'wdt '):       # Name
                ba.extend([code])

            ba.extend(struct.pack("d", wdt))    # WDT Value

        return ba

    @staticmethod
    def time_stamp_seconds(ens):
        """
        Calcualte the timestamp.  This is the number of seconds for the given
        date and time.
        :param ens: Ensemble to get the timestamp.
        :return: Timestamp in seconds.
        """

        ts = 0.0

        if ens.IsEnsembleData:
            year = ens.EnsembleData.Year
            month = ens.EnsembleData.Month
            day = ens.EnsembleData.Day
            hour = ens.EnsembleData.Hour
            minute = ens.EnsembleData.Minute
            second = ens.EnsembleData.Second
            hsec = ens.EnsembleData.HSec
            jdn = WaveForceCodec.julian_day_number(year, month, day)

            ts = (24.0 * 3600.0 * jdn) + (3600.0 * hour) + (60.0 * minute) + second + (hsec / 100.0)

        return ts

    @staticmethod
    def julian_day_number(year, month, day):
        """
        Count the number of calendar days there are for the given
        year, month and day.
        :param year: Years.
        :param month: Months.
        :param day: Days.
        :return: Number of days.
        """
        a = (14 - month) / 12
        y = year + 4800 - a
        m = month - 12 * a - 3

        return day + (153 * m + 2) / 5 + (365 * y) + y / 4 - y / 100 + y / 400 - 32045
