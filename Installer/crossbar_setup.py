from cx_Freeze import setup, Executable

setup(
    name = "Crossbar.io",
    version = "1.0.0",
    description = "Crossbar.IO",
    executables = [Executable("/usr/local/bin/crossbar")],
)