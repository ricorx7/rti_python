

# Load the files in the top level folder
import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


from AdcpSerialPortServer import AdcpSerialPortServer


if __name__ == '__main__':
    AdcpSerialPortServer("55056", '/dev/cu.usbserial-FTYNODPO', 115200)

