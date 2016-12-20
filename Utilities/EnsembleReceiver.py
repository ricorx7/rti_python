import socket
import sys, getopt


class EnsembleReceiver():
    """
    Create a TCP reader class
    """
    def __init__(self, udp_port):
        print("Ensemble Receiver: ", udp_port)
        self.port = udp_port
        self.socket = None
        self.reconnect(port)
        self.read()

    def reconnect(self, udp_port):
        """
        Connect to the server.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            self.socket.settimeout(10)
            self.socket.bind(('localhost', udp_port))
        except ConnectionRefusedError as err:
            print(err)
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
                response = self.socket.recvfrom(5120)
                print('"%s"' % str(response[0], "UTF-8"))

                if len(response) == 0:
                    print("Disconnected")

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
    reader = EnsembleReceiver(port)
    reader.close()
    print("Socket Closed")