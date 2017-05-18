import threading
import socket
import json
from log import logger


class ReadUdpPort:

    def __init__(self, udp_port):
        """
        Initialize the thread to read the data from the TCP port.
        """
        self.is_alive = True
        self.socket = None
        self.file_socket = None
        self.serial_server_thread = None
        self.udp_port = udp_port

        # Start a tcp connection to monitor incoming data and record
        self.serial_server_thread = threading.Thread(name='UDP Port Reader', target=self.connect(udp_port))
        self.serial_server_thread.start()

    def connect(self, udp_port):
        """
        Connect to the ADCP serial server.  This TCP server outputs data from
        the serial port.  Start reading the data.
        """
        try:
            # Create socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            self.socket.settimeout(10)
            self.socket.bind(('', udp_port))
            self.file_socket = self.socket.makefile()   # Convert to file, to use ReadLine

            # Start to read the raw data
            self.read_udp_socket()
        except ConnectionRefusedError as err:
            logger.error("Serial Send Socket: ", err)
            exit()
        except Exception as err:
            logger.error('Serial Send Socket: ", Error Opening socket', err)
            exit()

    def read_udp_socket(self):
        """
        Read the data from the TCP port.  This is the raw data from the serial port.
        """
        while self.is_alive:
            try:
                # Get the JSON data
                # Each dataset has a Newline added to the end to find the end of each dataset
                response = self.file_socket.readline()

                # JSON data
                json_response = json.loads(response)

                # Send the JSON data to the abstract class to process
                # the JSON data.
                #self.process(json_response)
                print(json_response)

                # Pass the data to the websocket


                # Check if disconnected
                if len(response) == 0:
                    logger.info("Disconnected")

                    # Close the socket
                    self.close()

                    # Reconnect to the server
                    self.connect(self.udp_port)

                    # Try to read again
                    self.read_udp_socket()
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

        print("Read Thread turned off")

    def close(self):
        """
        Stop the ADCP Serial UDP reader
        """
        # Stop the thread loop
        self.is_alive = False

        self.socket.close()

        logger.debug("Stop the UDP reader")


if __name__ == '__main__':
    tcp = ReadUdpPort(55057)

