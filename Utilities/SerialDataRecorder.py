import getopt
import logging
import sys
import socket
import threading

from Comm.AdcpSerialPortServer import AdcpSerialPortServer

logger = logging.getLogger("Ensemble File Report")
logger.setLevel(logging.ERROR)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class SerialDataRecorder:
    """
    Record the serial data.  This will work as a data logger.
    It will record the serial data and write it to the file path given.
    If no file path is given it will write it in the same directory as
    the application is run.
    """

    def __init__(self, verbose=False):
        self.serial_server = None
        self.serial_server_thread = None
        self.serial_writer_thread = None
        self.comm_port = ""
        self.baud = 0
        self.tcp_port = 0
        self.verbose = verbose
        self.folder_path = ''

        self.raw_serial_socket = None
        self.serial_buffer = bytearray()
        self.isAlive = True

    def connect(self, comm_port, baud, folder_path, tcp_port=55056):
        """
        Connect to the serial port to receive data.
        :param comm_port: Comm port to connect to.
        :param baud: Baud Rate.
        :param folder_path: Folder path to store the recorded data.
        :param tcp_port: TCP Port to receive the data.
        """
        self.comm_port = comm_port
        self.baud = baud
        self.tcp_port = tcp_port
        self.folder_path = folder_path
        self.serial_server = AdcpSerialPortServer(tcp_port,
                                                  comm_port,
                                                  baud)

        # Start a tcp connection to monitor incoming data and record
        self.serial_server_thread = threading.Thread(name='AdcpWriter',
                                                     target=self.create_raw_serial_socket(self.tcp_port))
        self.serial_server_thread.start()

    def create_raw_serial_socket(self, port):
        """
        Connect to the ADCP serial server.
        """
        try:
            self.raw_serial_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.raw_serial_socket.connect(('localhost', int(port)))
            self.raw_serial_socket.settimeout(1)    # Set timeout to stop thread if terminated
        except ConnectionRefusedError as err:
            print("Serial Send Socket: ", err)
        except Exception as err:
            print('Serial Send Socket: ", Error Opening socket', err)

        # Start a thread to read the raw data
        self.serial_writer_thread = threading.Thread(name='AdcpWriter',
                                                     target=self.create_raw_serial_socket(self.tcp_port))
        self.serial_writer_thread.start()

    def read_tcp_socket(self, data):
        """
        Run the loop to view data from the serial port.
        Emit the data so the view can view the data.

        """
        while self.isAlive:
            try:
                # Read data from socket
                data = self.raw_serial_socket.recv(4096)

                # If data exist process
                if len(data) > 0:
                    self.raw_data.emit(data)

            except socket.timeout:
                # Just a socket timeout, continue on
                pass

        print("Read Thread turned off")

    def stop_adcp_server(self):
        """
        Stop the ADCP Serial TCP server
        """
        if self.serial_server is not None:
            self.serial_server.close()
            print("serial server stopped")
        else:
            print('No serial connection')

        # Close the socket
        self.raw_serial_socket.close()

        if self.adcp_writer_thread is not None:
            self.adcp_writer_thread.join()

        if self.ensemble_reader_thread is not None:
            #self.ensemble_reader_thread.terminate()
            #self.ensemble_reader_thread.setTerminationEnabled(True)
            self.ensemble_reader_thread.stop()


def main(argv):
    comm_port = ''
    baud = '115200'
    tcp_port = '55056'
    folder_path = ''
    verbose = False
    try:
        opts, args = getopt.getopt(argv, "hlvc:b:f:p:", ["comm=", "baud=", "folder=", "tcp=", "verbose"])
    except getopt.GetoptError:
        print('EnsembleFileReport.py -c <comm> -b <baud> -f <folder> -p <tcp> -v')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: SerialDataRecorder.py ')
            print('-c <comm>\t : Serial Comm Port.  Use -l to list all the ports.')
            print('-b <baud>\t : Serial Baud Rate. Default 115200.')
            print('-p <tcp>\t : TCP Port to output the serial data.  Default 55056.  Change if used already.')
            print('-f <folder>\t : Folder path to store the serial data.  Default is same path as application.')
            print('-v\t : Verbose output.')
            print('Utilities:')
            print('-l\t : Print all available Serial Ports')
            sys.exit()
        elif opt == '-l':
            AdcpSerialPortServer.list_serial_ports()
            sys.exit()
        elif opt in ('-c', "--comm"):
            comm_port = arg
        elif opt in ("-b", "--baud"):
            baud = arg
        elif opt in ("-f", "--folder"):
            folder_path = arg
        elif opt in ("-p", "--tcp"):
            tcp_port = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
            print("Verbose ON")
    print('Comm Port: ', comm_port)
    print('Baud Rate: ', baud)
    print('TCP Port: ', tcp_port)
    print('Folder Path: ', folder_path)
    print("Available Serial Ports:")
    serial_list = AdcpSerialPortServer.list_serial_ports()

    # Verify a good serial port was given
    if comm_port in serial_list:
        # Run serial port
        SerialDataRecorder(verbose).connect(comm_port, baud, folder_path, tcp_port)
    else:
        print("----------------------------------------------------------------")
        print("BAD SERIAL PORT GIVEN")
        print("Please use -c to give a good serial port.")
        print("-l will give you a list of all available serial ports.")

if __name__ == "__main__":
    main(sys.argv[1:])

