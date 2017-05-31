# rti-python
RTI Library in Python


Rowe Technologies Inc. Python library

There is currently no main file to run.  This library contains a variety
of utility applications.  But there is no main application to run.

Dependicencies
------------

```python
pip3 install -r requirements.txt -UI
```

WAMP Application to run
-----------------------
```javascript
cd crossbar
crossbar start
```

This will start the WAMP server, the serial port and GUI


Compile QT5 .UI files
---------------------
```javascript
pyuic5 -x file.ui -o file.py
```


Run Utilties Apps
----------------
OSX and Linux
```javascript
export PYTHONPATH=$PYTHONPATH:/path/to/rti_python

python3 Utilities/EnsembleFileReport.py -i file -v
```

Windows
```javascript
set PYTHONPATH=%PYTHONPATH%;/path/to/rti_python
```

AWS DynamoDB
----------------
Install AWS CLI

```javascript
pip3 install awscli
```

Setup a configuration

```javascript
aws configure
```

Add a User to IAM in AWS Console

Create Access key and Secret key and add to 'aws configure'


-------------
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
