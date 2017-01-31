import struct
import socket
import datetime
import requests
import pickle
from Utilities.events import EventHandler

from Ensemble.Ensemble import Ensemble
from Ensemble.BeamVelocity import BeamVelocity
from Ensemble.InstrumentVelocity import InstrumentVelocity
from Ensemble.EarthVelocity import EarthVelocity
from Ensemble.Amplitude import Amplitude
from Ensemble.Correlation import Correlation
from Ensemble.GoodBeam import GoodBeam
from Ensemble.GoodEarth import GoodEarth
from Ensemble.EnsembleData import EnsembleData
from Ensemble.AncillaryData import AncillaryData
from Ensemble.BottomTrack import BottomTrack
from Ensemble.RangeTracking import RangeTracking

from PyCRC.CRCCCITT import CRCCCITT

from log import logger


class EnsembleMetaData:
    """
    Meta Data for the ensemble.
    THis includes the revision and host information.
    """
    def __init__(self):
        self.Revision = "1.0"
        self.Host = socket.gethostname()
        self.HostIp = socket.gethostbyname(socket.gethostname())

        # Get the external IP address of the computer
        #url = "http://checkip.dyndns.org"
        #request = requests.get(url)
        #clean = request.text.split(': ', 1)[1]
        #your_ip = clean.split('</body></html>', 1)[0]
        #self.HostExtIp = your_ip


class ProjectInfo:
    """
    Information about the project that collected this data.
    """
    def __init__(self):
        self.ProjectName = ""
        self.Username = ""
        self.Lat = ""
        self.Lon = ""
        self.DateCreated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self.DateModified = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


class WaveBurstInfo:
    """
    Information about the waves burst setup.
    """

    def __init__(self):
        self.SamplesPerBurst = 0
        self.Lat = ""
        self.Lon = ""
        self.Bin1 = 0
        self.Bin2 = 0
        self.Bin3 = 0


class BinaryCodec:
    """
    Decode RoweTech ADCP Binary data.
    """

    def __init__(self, udp_port):
        logger.debug("Binary codec - UDP Port: " + str(udp_port))
        self.buffer = bytearray()

        self.EnsembleEvent = EventHandler(self)

        # Set meta data
        self.Meta = EnsembleMetaData()

        # Set ProjectInfo
        #self.ProjectInfo = ProjectInfo()

        # Create socket
        self.udp_port = udp_port                                        # UDP Port
        self.udp_ip = '127.0.0.1'                                       # UDP IP (Localhost)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP Socket

    def add(self, data):
        """
        Add to buffer and Decode
        :param data: Raw byte data.
        """
        self.buffer.extend(data)

        self.find_ensemble()

    def find_ensemble(self):
        """
        Find the start of an ensemble.  Then find the end of the ensemble.
        Then remove the ensemble from the buffer and process the raw data.
        :return:
        """

        # Look for first 16 bytes of header
        delimiter = b'\x80'*16
        ens_start = self.buffer.find(delimiter)

        if ens_start >= 0 and len(self.buffer) > Ensemble().HeaderSize + ens_start:
            # Decode the Ensemble
            self.decode_ensemble(ens_start)

    def decode_ensemble(self, ensStart):
        """
        Decode the raw ensemble data.  This will check the checksum and verify it is correct,
        then decode each datasets.  Then remove the data from the buffer.
        :param ensStart: Stare of the ensemble in the buffer.
        """

        # Check Ensemble number
        ensNum = struct.unpack("I", self.buffer[ensStart+16:ensStart+20])
        #print(ensNum[0])
        #print(self.ones_complement(ensNumInv[0]))


        # Check ensemble size
        payloadSize = struct.unpack("I", self.buffer[ensStart+24:ensStart+28])
        #print(payloadSize[0])
        #payloadSizeInv = struct.unpack("I", self.buffer[ensStart+28:ensStart+32])
        #print(self.ones_complement(payloadSizeInv[0]))

        # Ensure the entire ensemble is in the buffer
        if len(self.buffer) >= ensStart + Ensemble().HeaderSize + payloadSize[0] + Ensemble().ChecksumSize:
            # Check checksum
            checksumLoc = ensStart + Ensemble().HeaderSize + payloadSize[0]
            checksum = struct.unpack("I", self.buffer[checksumLoc:checksumLoc + Ensemble().ChecksumSize])

            # Calculate Checksum
            # Use only the payload for the checksum
            ens = self.buffer[ensStart + Ensemble().HeaderSize:ensStart + Ensemble().HeaderSize + payloadSize[0]]
            calcChecksum = CRCCCITT().calculate(input_data=bytes(ens))
            #print("Calc Checksum: ", calcChecksum)
            #print("Checksum: ", checksum[0])
            #print("Checksum good: ", calcChecksum == checksum[0])

            if checksum[0] == calcChecksum:
                logger.debug(ensNum[0])
                # Decode data
                ensemble = self.decode_data_sets(self.buffer[ensStart:ensStart + Ensemble().HeaderSize + payloadSize[0]])

                # ************************
                try:
                    # Stream data
                    self.stream_data(ensemble)

                    logger.debug("Stream ensemble data")
                except ConnectionRefusedError as err:
                    logger.error("Error streaming ensemble data", err)
                except Exception as err:
                    logger.error("Error streaming ensemble data", err)

                # Pass to event handler
                self.EnsembleEvent(ensemble)

            # Remove ensemble from buffer
            ensEnd = ensStart + Ensemble().HeaderSize + payloadSize[0] + Ensemble().ChecksumSize
            del self.buffer[0:ensEnd]

    def decode_data_sets(self, ens):
        """
        Decode the datasets in the ensemble.
        :param ens: Ensemble data.  Decode the dataset.
        :return: Return the decoded ensemble.
        """
        #print(ens)
        packetPointer = Ensemble().HeaderSize
        type = 0
        numElements = 0
        elementMultiplier = 0
        imag = 0
        nameLen = 0
        name = ""
        dataSetSize = 0

        # Create the ensemble
        ensemble = Ensemble()

        # Add the raw data to the ensemble
        #ensemble.AddRawData(ens)

        # Decode the ensemble datasets
        for x in range(Ensemble().MaxNumDataSets):
            # Check if we are at the end of the payload
            if packetPointer >= len(ens):
                break;

            # Get the dataset info
            ds_type = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 0), Ensemble().BytesInInt32, ens)
            num_elements = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 1), Ensemble().BytesInInt32, ens)
            element_multiplier = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 2), Ensemble().BytesInInt32, ens)
            image = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 3), Ensemble().BytesInInt32, ens)
            name_len = Ensemble.GetInt32(packetPointer + (Ensemble.BytesInInt32 * 4), Ensemble().BytesInInt32, ens)
            name = str(ens[packetPointer+(Ensemble.BytesInInt32 * 5):packetPointer+(Ensemble.BytesInInt32 * 5)+8], 'UTF-8')

            # Calculate the dataset size
            data_set_size = Ensemble.GetDataSetSize(ds_type, name_len, num_elements, element_multiplier)

            # Beam Velocity
            if "E000001" in name:
                logger.debug(name)
                bv = BeamVelocity(num_elements, element_multiplier)
                bv.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddBeamVelocity(bv)

            # Instrument Velocity
            if "E000002" in name:
                logger.debug(name)
                iv = InstrumentVelocity(num_elements, element_multiplier)
                iv.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddInstrumentVelocity(iv)

            # Earth Velocity
            if "E000003" in name:
                logger.debug(name)
                ev = EarthVelocity(num_elements, element_multiplier)
                ev.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddEarthVelocity(ev)

            # Amplitude
            if "E000004" in name:
                logger.debug(name)
                amp = Amplitude(num_elements, element_multiplier)
                amp.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddAmplitude(amp)

            # Correlation
            if "E000005" in name:
                logger.debug(name)
                corr = Correlation(num_elements, element_multiplier)
                corr.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddCorrelation(corr)

            # Good Beam
            if "E000006" in name:
                logger.debug(name)
                gb = GoodBeam(num_elements, element_multiplier)
                gb.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddGoodBeam(gb)

            # Good Earth
            if "E000007" in name:
                logger.debug(name)
                ge = GoodEarth(num_elements, element_multiplier)
                ge.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddGoodEarth(ge)

            # Ensemble Data
            if "E000008" in name:
                logger.debug(name)
                ed = EnsembleData(num_elements, element_multiplier)
                ed.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddEnsembleData(ed)

            # Ancillary Data
            if "E000009" in name:
                logger.debug(name)
                ad = AncillaryData(num_elements, element_multiplier)
                ad.decode(ens[packetPointer:packetPointer+data_set_size])
                ensemble.AddAncillaryData(ad)

            # Bottom Track
            if "E000010" in name:
                logger.debug(name)
                bt = BottomTrack(num_elements, element_multiplier)
                bt.decode(ens[packetPointer:packetPointer + data_set_size])
                ensemble.AddEnsembleData(bt)

            # Range Tracking
            if "E000015" in name:
                logger.debug(name)
                rt = RangeTracking(num_elements, element_multiplier)
                rt.decode(ens[packetPointer:packetPointer + data_set_size])
                ensemble.AddRangeTracking(rt)

            # Move to the next dataset
            packetPointer += data_set_size

        return ensemble

    def stream_data(self, ens):
        """
        Stream the data to the UDP port.
        When converting the dataset to JSON, a newline will be added
        to end of the JSON string.  This will allow the user to separate
        the JSON strings.
        :param ens: Ensemble data to stream.
        """
        serial_number = ""
        ensemble_number = 0
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        if ens.IsEnsembleData:
            # Get the serial number, ensemble number and the date and time to share with all the data
            serial_number = ens.EnsembleData.SerialNumber
            ensemble_number = ens.EnsembleData.EnsembleNumber
            date_time = datetime.datetime(year=ens.EnsembleData.Year,
                                          month=ens.EnsembleData.Month,
                                          day=ens.EnsembleData.Day,
                                          hour=ens.EnsembleData.Hour,
                                          minute=ens.EnsembleData.Minute,
                                          second=ens.EnsembleData.Second,
                                          microsecond=round(ens.EnsembleData.HSec*10000)).strftime("%Y-%m-%d %H:%M:%S.%f")

            # Stream the data
            ens.EnsembleData.DateTime = date_time
            ens.EnsembleData.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.EnsembleData).encode())

        if ens.IsBeamVelocity:
            ens.BeamVelocity.EnsembleNumber = ensemble_number
            ens.BeamVelocity.SerialNumber = serial_number
            ens.BeamVelocity.DateTime = date_time
            ens.BeamVelocity.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.BeamVelocity).encode())

        if ens.IsInstrumentVelocity:
            ens.InstrumentVelocity.EnsembleNumber = ensemble_number
            ens.InstrumentVelocity.SerialNumber = serial_number
            ens.InstrumentVelocity.DateTime = date_time
            ens.InstrumentVelocity.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.InstrumentVelocity).encode())

        if ens.IsEarthVelocity:
            ens.EarthVelocity.EnsembleNumber = ensemble_number
            ens.EarthVelocity.SerialNumber = serial_number
            ens.EarthVelocity.DateTime = date_time
            ens.EarthVelocity.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.EarthVelocity).encode())

        if ens.IsAmplitude:
            ens.Amplitude.EnsembleNumber = ensemble_number
            ens.Amplitude.SerialNumber = serial_number
            ens.Amplitude.DateTime = date_time
            ens.Amplitude.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.Amplitude).encode())

        if ens.IsCorrelation:
            ens.Correlation.EnsembleNumber = ensemble_number
            ens.Correlation.SerialNumber = serial_number
            ens.Correlation.DateTime = date_time
            ens.Correlation.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.Correlation).encode())

        if ens.IsGoodBeam:
            ens.GoodBeam.EnsembleNumber = ensemble_number
            ens.GoodBeam.SerialNumber = serial_number
            ens.GoodBeam.DateTime = date_time
            ens.GoodBeam.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.GoodBeam).encode())

        if ens.IsGoodEarth:
            ens.GoodEarth.EnsembleNumber = ensemble_number
            ens.GoodEarth.SerialNumber = serial_number
            ens.GoodEarth.DateTime = date_time
            ens.GoodEarth.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.GoodEarth).encode())

        if ens.IsAncillaryData:
            ens.AncillaryData.EnsembleNumber = ensemble_number
            ens.AncillaryData.SerialNumber = serial_number
            ens.AncillaryData.DateTime = date_time
            ens.AncillaryData.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.AncillaryData).encode())

        if ens.IsBottomTrack:
            ens.BottomTrack.EnsembleNumber = ensemble_number
            ens.BottomTrack.SerialNumber = serial_number
            ens.BottomTrack.DateTime = date_time
            ens.BottomTrack.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.BottomTrack).encode())

        if ens.IsRangeTracking:
            ens.RangeTracking.EnsembleNumber = ensemble_number
            ens.RangeTracking.SerialNumber = serial_number
            ens.RangeTracking.DateTime = date_time
            ens.RangeTracking.Meta = self.Meta
            self.send_udp(Ensemble().toJSON(ens.RangeTracking).encode())

    def send_udp(self, data):
        """
        Send the data to the UDP port.
        Ensemble().toJSON added a newline at the end of the JSON
        string.  This will allow anyone looking for the JSON data
        to separate the JSON data by newline.
        :param data: Data to send.
        """
        self.socket.sendto(data, (self.udp_ip, self.udp_port))



