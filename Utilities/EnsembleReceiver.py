import socket
import sys, getopt
import json
import abc
import logging

logger = logging.getLogger("EnsembleReceiver")
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class EnsembleReceiver():
    """
    Create a UDP reader class
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.port = 55057   # Default port
        self.socket = None


    def connect(self, udp_port):
        """
        Connect to the UDP port and begin reading data.
        """
        self.port = udp_port
        logger.info("Ensemble Receiver: " + str(udp_port))

        self.reconnect(self.port)
        self.read()

    def reconnect(self, udp_port):
        """
        Connect to the server.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            self.socket.settimeout(10)
            self.socket.bind(('localhost', udp_port))
            self.file_socket = self.socket.makefile()
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
        while True:
            try:
                # Receive a response
                #response = self.socket.recvfrom(5120)
                response = self.file_socket.readline()
                #print('"%s"' % str(response[0], "UTF-8"))
                #print(response)
                jsonResponse = json.loads(response)
                #print(jsonResponse)
                #logger.info(jsonResponse["Name"])

                # Send the JSON data to the abstract class to process
                # the JSON data.
                self.process(jsonResponse)


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
                break
            except socket.timeout:
                # Do nothing
                continue

    def close(self):
        """
        Close the socket.
        """
        self.socket.close()

    @abc.abstractmethod
    def process(self, jsonData):
        """
        Process the JSON data.
        :param jsonData: JSON data.
        """
        #return

if __name__ == '__main__':
    argv = sys.argv[1:]
    port = 55057
    try:
        opts, args = getopt.getopt(argv,"p:",["port="])
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