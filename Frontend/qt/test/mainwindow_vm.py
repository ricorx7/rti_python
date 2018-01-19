import sys

from PyQt5 import QtWidgets

from mainwindow import Ui_MainWindow


class MyFirstGuiProgram(Ui_MainWindow):
    def __init__(self, dialog):
        Ui_MainWindow.__init__(self)
        self.setupUi(dialog)

        # Connect "add" button with a custom function (addInputTextToListbox)
        self.pushButton.clicked.connect(self.addInputTextToListbox)

    def addInputTextToListbox(self):
        #txt = self.myTextInput.text()
        #self.listWidget.addItem(txt)
        print("test")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = QtWidgets.QMainWindow()

    prog = MyFirstGuiProgram(dialog)

    dialog.show()
    sys.exit(app.exec_())