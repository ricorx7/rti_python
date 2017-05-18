import threading
import socket
import sys
import getopt
from log import logger
from Codecs.AdcpCodec import AdcpCodec
from Comm.AdcpSerialPortServer import  AdcpSerialPortServer


class DecodeSerialData:

    def __init__(self, tcp_port, comm_port, baud):
        """
        Initialize the thread to read the data from the TCP port.
        """
        self.is_alive = True
        self.raw_serial_socket = None
        self.serial_server_thread = None

        # Create the codec
        self.codec = AdcpCodec()

        # Create a serial port server to read data from the
        # serial port and pass it on TCP
        self.serial_server = AdcpSerialPortServer(str(tcp_port),
                                                  comm_port,
                                                  baud)

        # Start a tcp connection to monitor incoming data and decode
        self.serial_server_thread = threading.Thread(name='AdcpDecoder', target=self.create_raw_serial_socket(tcp_port))
        self.serial_server_thread.start()

    def create_raw_serial_socket(self, port):
        """
        Connect to the ADCP serial server.  This TCP server outputs data from
        the serial port.  Start reading the data.
        """
        try:
            # Create socket
            self.raw_serial_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.raw_serial_socket.connect(('localhost', int(port)))
            self.raw_serial_socket.settimeout(1)    # Set timeout to stop thread if terminated

            # Start to read the raw data
            self.read_tcp_socket()
        except ConnectionRefusedError as err:
            logger.error("Serial Send Socket: ", err)
            exit()
        except Exception as err:
            logger.error('Serial Send Socket: ", Error Opening socket', err)
            exit()

    def read_tcp_socket(self):
        """
        Read the data from the TCP port.  This is the raw data from the serial port.
        """
        while self.is_alive:
            try:
                # Read data from socket
                data = self.raw_serial_socket.recv(4096)

                # If data exist process
                if len(data) > 0:
                    # Send the data received to the codec
                    self.codec.add(data)

            except socket.timeout:
                # Just a socket timeout, continue on
                pass
            except Exception as e:
                logger.error("Exception in reading data.", e)
                self.stop_adcp_server()

        print("Read Thread turned off")

    def stop_adcp_server(self):
        """
        Stop the ADCP Serial TCP server
        """
        # Stop the thread loop
        self.is_alive = False

        if self.serial_server is not None:
            self.serial_server.close()
            logger.debug("serial server stopped")
        else:
            logger.debug('No serial connection')

        # Close the socket
        self.raw_serial_socket.close()

        # Stop the server thread
        if self.serial_server_thread is not None:
            self.serial_server_thread.join()

        # Close the open file
        self.close_file_write()

        logger.debug("Stop the Recorder")


def main(argv):
    tcp_port = "55056"
    comm_port = '/dev/tty.usbserial-FT0ED8ZR'
    baud = 115200

    try:
        opts, args = getopt.getopt(argv,"hlt:c:b:", [])
    except getopt.GetoptError:
        print('test_DecodeSerialData.py -t <tcp_port> -c <comm> -b <baud>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test_DecodeSerialData.py -t <tcp_port> -c <comm> -b <baud>')
            sys.exit()
        elif opt in ("-l"):
            print("Available Serial Ports:")
            AdcpSerialPortServer.list_serial_ports()
            exit()
        elif opt in ('-t'):
            tcp_port = arg
        elif opt in ("-c"):
            comm_port = arg
        elif opt in ("-b"):
            baud = int(arg)

        # Get a list of all the serial ports available
        print("Available Serial Ports:")
        serial_list = AdcpSerialPortServer.list_serial_ports()

        print("TCP Port: " + tcp_port)
        print("Comm Port: " + comm_port)
        print("Baud rate: " + str(baud))

        # Verify a good serial port was given
        if comm_port in serial_list:
            # Run serial port
            sdr = DecodeSerialData(tcp_port, comm_port, baud)
            sdr.stop_adcp_server()
        else:
            print("----------------------------------------------------------------")
            print("BAD SERIAL PORT GIVEN")
            print("Please use -c to give a good serial port.")
            print("-l will give you a list of all available serial ports.")

if __name__ == "__main__":
    main(sys.argv[1:])