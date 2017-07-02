import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import qdarkstyle

from twisted.logger import Logger
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.wamp import ApplicationRunner

from predictor_vm import PredictorVM


class MainWindow(ApplicationSession, QtWidgets.QMainWindow):
    """
    Main window for the application
    """

    def __init__(self, config=None):
        ApplicationSession.__init__(self, config)
        QtWidgets.QMainWindow.__init__(self)

        # Setup logger
        log = Logger()

        # Initialize the pages
        self.predictor = PredictorVM(self)

        # Initialize the window
        self.main_window_init()

    def main_window_init(self):
        # Show the main window
        self.show()

    @inlineCallbacks
    def onJoin(self, details):
        self.log.info("WAMP connected")
        # WAMP onJoin
        yield self.subscribe(None, u"com.rti.data.serial")

        # Initialize the WAMP components with the Widgets
        #self.adcp_term.wamp_init()

    def closeEvent(self, event):
        """
        Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Close, Cancel buttons
        """
        reply = QtWidgets.QMessageBox.question(self, "Message",
            "Are you sure you want to quit?", QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Cancel)

        if reply == QtWidgets.QMessageBox.Close:

            # Stop Reactor
            from twisted.internet import reactor
            if reactor.running:
                reactor.stop()

            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    is_wamp= False

    if is_wamp:
        #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        import qt5reactor

        # Add PyQT5 to twisted reactor
        qt5reactor.install()

        # Start the WAMP connection
        # Connect the main window to the WAMP connection
        runner = ApplicationRunner(url=u"ws://localhost:55058/ws", realm=u"realm1")
        runner.run(MainWindow, auto_reconnect=True)

    else:
        #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        MainWindow()
        sys.exit(app.exec_())
