from cx_Freeze import setup, Executable

setup(
    name="Process Waves Data",
    version="0.1",
    description="Process Waves Data application",
    executables=[Executable("../Utilities/ProcessWavesFile.py")],
)
