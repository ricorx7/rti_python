

import sys
import socket
import glob
from PySide2 import QtCore, QtGui, QtWidgets
from AdcpSerialPortServer import AdcpSerialPortServer
import serial
import threading
from Ensemble import EnsembleReader

class view_serial(QtWidgets.QWidget):
    """
    Create the QT display
    """
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)

        self.serial_server = None
        self.serial_send_socket = None
        self.ensemble_reader_thread = None
        self.adcp_writer_thread = None

        self.tcp_port_combobox = QtWidgets.QComboBox()
        self.tcp_port_combobox.setEditable(True)
        self.tcp_port_combobox.addItems(["55056", ""])

        self.comm_port_combobox = QtWidgets.QComboBox()
        self.comm_port_combobox.addItems(self.serial_ports())

        self.comm_baud_combobox = QtWidgets.QComboBox()
        self.comm_baud_combobox.setEditable(True)
        self.comm_baud_combobox.addItems(["921600", "115200", "19200", ""])
        self.comm_baud_combobox.setCurrentIndex(1)

        connect = QtWidgets.QPushButton("Connect")
        connect.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        connect.clicked.connect(self.start_adcp_server)

        disconnect = QtWidgets.QPushButton("Reconnect")
        disconnect.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        disconnect.clicked.connect(self.reconnect_adcp_server)

        self.command_txtbox = QtWidgets.QLineEdit()

        send_cmd_btn = QtWidgets.QPushButton("Send")
        send_cmd_btn.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        send_cmd_btn.clicked.connect(self.send_cmd_adcp_server)

        quit = QtWidgets.QPushButton("Quit")
        quit.setFont(QtGui.QFont("Times", 18, QtGui.QFont.Bold))
        self.connect(quit, QtCore.SIGNAL("clicked()"),
                     QtWidgets.qApp, QtCore.SLOT("quit()"))



        gridLayout = QtWidgets.QGridLayout()
        gridLayout.addWidget(self.tcp_port_combobox, 0, 0)
        gridLayout.addWidget(self.comm_port_combobox, 1, 0)
        gridLayout.addWidget(self.comm_baud_combobox, 1, 1)
        gridLayout.addWidget(connect, 2, 0)
        gridLayout.addWidget(disconnect, 2, 1)
        gridLayout.addWidget(self.command_txtbox, 3, 0)
        gridLayout.addWidget(send_cmd_btn, 3, 1)
        gridLayout.addWidget(quit, 4, 0)

        gridLayout.setColumnStretch(1, 10)
        self.setLayout(gridLayout)

    def closeEvent(self, event):
        """
        Override the close event for the QWidget.
        If a serial port is open, close the connection.
        """
        print('Closing serial')
        self.stop_adcp_server()
        # Close window
        event.accept()

    def start_adcp_server(self):
        """
        Start the ADCP Serial TCP server
        """

        self.serial_server = AdcpSerialPortServer(self.get_tcp_port(),
                                                  self.comm_port_combobox.currentText(),
                                                  self.get_baud())

        # Create an ensemble reader
        #self.ensemble_reader_thread = threading.Thread(name='EnsembleReader', target=EnsembleReader.EnsembleReader(self.get_tcp_port())).start()

        # Connect to serial server to send commands
        self.adcp_writer_thread = threading.Thread(name='AdcpWriter', target=self.create_send_socket(self.get_tcp_port())).start()

        print("start server")

    def create_send_socket(self, port):
        """
        Connect to the ADCP serial server.
        """
        try:
            self.serial_send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serial_send_socket.connect(('localhost', int(port)))
        except ConnectionRefusedError as err:
            print("Serial Send Socket: ", err)
        except:
            print('Serial Send Socket: ", Error Opening socket')

    def stop_adcp_server(self):
        """
        Stop the ADCP Serial TCP server
        """
        if self.serial_server is not None:
            self.serial_server.close()
            print("serial server stopped")
        else:
            print('No serial connection')

        if self.adcp_writer_thread is not None:
            self.adcp_writer_thread.join()


    def send_cmd_adcp_server(self):
        """
        Send the command to the socket
        """
        # Get the command from the txtbox
        cmd = self.command_txtbox.text().strip()

        # Encode the data to byte array and send to socket
        self.serial_send_socket.send((cmd.strip()).encode())

    def reconnect_adcp_server(self):
        """
        Reconnect the serial port connection with the new
        settings.
        """
        print("reconnect")

    def get_baud(self):
        """
        Convert the baud rate from string to int.
        If an error, set the baud rate to 115200

        :returns: baud rate
        """
        try:
            baud = int(self.comm_baud_combobox.currentText())
        except:
            self.comm_baud_combobox.setCurrentIndex(1)
            return "115200"

        return baud

    def get_tcp_port(self):
        """
        Convert the TCP port from string to int.
        If an error, set the default port to 55056

        :returns: baud rate
        """
        try:
            port = int(self.tcp_port_combobox.currentText())
        except:
            self.tcp_port_combobox.setCurrentIndex(0)
            return "55056"

        return str(port)

    def serial_ports(self):
        """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def find_port(self):
        """
        Finds available port for Tornado / Flask
        :return: Available port
        :rtype: int
        """

        port_attempts = 0
        while port_attempts < 1000:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('localhost', 0))
                app_port = sock.getsockname()[1]
                sock.close()
                print("PORT: " + str(app_port))
                return app_port
            except:
                port_attempts += 1

        print("FAILED AFTER 1000 PORT ATTEMPTS")
        sys.exit(1)
