from cx_Freeze import setup, Executable


setup(
    name = "AdcpTerminal",
    version = "1.0.0",
    description = "Setup the Terminal and connection to crossbar.io",
    executables = [Executable("../Frontend/qt/mainwindow.py")],
)
