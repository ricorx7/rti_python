# rti-python
RTI Library in Python


RoweTech Inc Python library

Dependicencies
------------

pip3 install pyserial
install pyside2



#install pyside2

#To Compile pyside2 from source for OSX

##Download and install QT5.6
```
curl -O https://raw.githubusercontent.com/Homebrew/homebrew-core/fdfc724dd532345f5c6cdf47dc43e99654e6a5fd/Formula/qt5.rb
```
```
brew install ./qt5.rb
```
##Download pyside2
```
git clone --recursive http://code.qt.io/cgit/pyside/pyside-setup.git/
```

##Install pyside3 with python3 and QT5.6
```
python3 setup.py install ---ignore-git --build-tests --qmake=/usr/local/Cellar/qt5/5.6.1-1/bin/qmake --cmake=/usr/local/bin/cmake --openssl=/usr/bin/openssl
```
