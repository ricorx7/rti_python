# -*- mode: python -*-

block_cipher = None


a = Analysis(['mainwindow.py'],
             pathex=['C:\\Users\\rico\\AppData\\Roaming\\Python\\Python35\\site-packages\\PyQt5\\Qt\\bin', 'G:\\rti\\python\\rti_python'],
             binaries=[],
             datas=[('rti_python/ADCP/Predictor/predictor.json', 'ADCP/Predictor/.'), ('rti.ico', '.'), ('rti_python/ADCP/AdcpCommands.json', 'ADCP/.')],
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
          name='PredictR',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='rti.ico')
