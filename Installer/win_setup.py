from cx_Freeze import setup, Executable

setup(
    name = "WampADCP",
    version = "1.0.0",
    description = "Setup the Terminal and connection to crossbar.io",
    executables = [Executable("../Wamp/WampAdcp.py")],
)