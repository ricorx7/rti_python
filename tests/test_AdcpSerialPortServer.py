import os
import sys
import getopt

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from Comm.AdcpSerialPortServer import AdcpSerialPortServer

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hl", [])
    except getopt.GetoptError:
        print('EnsembleFileReport.py -i <inputfile> -v')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test_AdcpSerialPortServer.py ')
            sys.exit()
        elif opt in ("-l"):
            print("Available Serial Ports:")
            serial_list = AdcpSerialPortServer.list_serial_ports()
            exit()

    # Start the server
    AdcpSerialPortServer("55056", '/dev/tty.usbserial-FT0ED8ZR', 115200)

if __name__ == "__main__":
    main(sys.argv[1:])
