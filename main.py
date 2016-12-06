

import sys
from AdcpSerialPortServer import AdcpSerialPortServer
from PySide2 import QtCore, QtGui, QtWidgets
from view_main import view_main


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = view_main()
    widget.setGeometry(100, 100, 500, 355)
    widget.show()
    sys.exit(app.exec_())



