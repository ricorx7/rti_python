# -*- mode: python -*-

block_cipher = None


a = Analysis(['Frontend/qt/Predictor/mainwindow.py'],
             pathex=['/Users/rico/python/rti_python'],
             binaries=[],
             datas=[('ADCP/Predictor/predictor.json', 'ADCP/Predictor/.'), ('Updater/rti.ico', 'Updater/.'), ('ADCP/AdcpCommands.json', 'ADCP/.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='mainwindow',
          debug=False,
          strip=False,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='PredictR.app',
             icon='Updater/rti.ico',
             bundle_identifier=None)
