import socket
import sys, getopt
import json
import abc
from log import logger
from Utilities.events import EventHandler
from Comm.EnsembleJsonData import EnsembleJsonData

import configparser
settings = configparser.ConfigParser()
settings._interpolation = configparser.ExtendedInterpolation()
settings.read('settings.ini')


class EnsembleReceiver:
    """
    Create a UDP reader class
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.port = int(settings.get('SerialServerSection', 'JsonEnsUdpPort'))   # Default port
        self.socket = None
        self.file_socket = None
        self.is_alive = False
        self.adcp_data = EnsembleJsonData()
        self.EnsembleEvent = EventHandler(self)     # Event to handle a complete JSON ensemble

    def connect(self, udp_port):
        """
        Connect to the UDP port and begin reading data.
        """
        self.is_alive = True
        self.port = udp_port
        logger.info("Ensemble Receiver: " + str(udp_port))

        self.reconnect(self.port)
        self.read()

    def reconnect(self, udp_port):
        """
        Connect to the server.
        """
        try:
            self.is_alive = True
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            self.socket.settimeout(10)
            self.socket.bind(('', udp_port))
            self.file_socket = self.socket.makefile()   # Convert to file, to use ReadLine
        except ConnectionRefusedError as err:
            logger.error(err)
            sys.exit(2)
        except Exception as err:
            print('Error Opening socket: ', err)
            sys.exit(2)

    def read(self):
        """
        Read data from the serial port
        """
        while self.is_alive:
            try:
                # Get the JSON data
                # Each dataset has a Newline added to the end to find the end of each dataset
                response = self.file_socket.readline()

                # JSON data
                json_response = json.loads(response)
                #logger.debug(jsonResponse["Name"])

                # Send the JSON data to the abstract class to process
                # the JSON data.
                self.process(json_response)

                # Check if disconnected
                if len(response) == 0:
                    logger.info("Disconnected")

                    # Close the socket
                    self.close()

                    # Reconnect to the server
                    self.reconnect(self.port)

                    # Try to read again
                    self.read()
            except KeyboardInterrupt:
                # Ctrl-C will stop the application
                logger.info("Keyboard interrupt stopped app")
                self.close()
                break
            except socket.timeout:
                # Do nothing
                continue
            except OSError as ex:
                logger.error("Socket is timed out.", ex)
                return
            except Exception as ex:
                logger.error("Error receiving ensemble data. ", ex)
                return

    def close(self):
        """
        Close the socket.
        """
        self.is_alive = False
        self.socket.close()

    @abc.abstractmethod
    def process(self, json_data):
        """
        Process the JSON data.
        :param json_data: JSON data.
        """

        if json_data["EnsembleNumber"] == self.adcp_data.EnsembleNumber:
            # Add the JSON data to the ensemble data
            self.adcp_data.process(json_data)
        else:
            # Send the completed ensemble to the event handler
            self.EnsembleEvent(self.adcp_data)

            # Create the new JSON ensemble
            self.adcp_data = EnsembleJsonData()
            self.adcp_data.EnsembleNumber = json_data["EnsembleNumber"]
            self.adcp_data.process(json_data)

        #self.EnsembleEvent(json_data)
        return json_data

if __name__ == '__main__':
    argv = sys.argv[1:]
    port = 55057
    try:
        opts, args = getopt.getopt(argv, "p:", ["port="])
    except getopt.GetoptError:
        print('EnsembleReceiver.py  -p <port>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('EnsembleReceiver.py -p <port>')
            sys.exit()
        elif opt in ("-p", "--port"):
            port = int(arg)

    # Read from TCP port
    reader = EnsembleReceiver()
    reader.connect(port)
    reader.close()
    logger.info("Socket Closed")