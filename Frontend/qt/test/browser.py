import sys
from PyQt5.QtCore import QEventLoop, QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

class Browser(QWebEngineView):
    def __init__(self):
        # QWebView
        self.view = QWebEngineView.__init__(self)
        self.setWindowTitle('Loading...')
        self.titleChanged.connect(self.adjustTitle)

        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        settings.setAttribute(QWebEngineSettings.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.HyperlinkAuditingEnabled, True)
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)

    def load(self, url):
        self.setUrl(QUrl(url))

    def adjustTitle(self):
        self.setWindowTitle(self.title())

    def disableJS(self):
        settings = QWebEngineSettings.globalSettings()
        settings.setAttribute(QWebEngineSettings.JavascriptEnabled, False)