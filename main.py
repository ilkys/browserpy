import sys
import keyboard
from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('CLeaRBrowser')
        self.setWindowIcon(QtGui.QIcon('ClearBrowser\ico\ico.ico'))
        self.showMaximized()
        self.show()

        self.browser = QWebEngineView()
        self.tabWidget = QTabWidget()
        self.tabWidget.setTabShape(QTabWidget.Triangular)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.close_Tab)
        self.setCentralWidget(self.tabWidget)

        self.webview = WebEngineView(self)
        self.webview.load(QUrl('about:blank'))
        self.create_tab(self.webview)

        navigation_bar = QToolBar('Navigation')

        navigation_bar.setIconSize(QSize(16, 16))

        self.addToolBar(navigation_bar)
        keyboard.add_hotkey("ctrl+t", lambda: self.create_tab())
        keyboard.add_hotkey("ctrl+w", lambda: self.close_tab())

        keyboard.add_hotkey("f5", lambda: self.webview.reload)

        back_button = QAction(QIcon(r'ClearBrowser\ico\back.png'), 'Back', self)
        next_button = QAction(QIcon(r'ClearBrowser\ico\forward.png'), 'Forward', self)
        add_button = QAction(QIcon(r'ClearBrowser\ico\yandex.png'), 'Google', self)
        reload_button = QAction(QIcon(r'ClearBrowser\ico\reload.png'), 'Reload', self)
        self.webview.load(QUrl("http://www.google.com"))

        back_button.triggered.connect(self.webview.back)
        next_button.triggered.connect(self.webview.forward)
        add_button.triggered.connect(lambda: self.create_tab(self.webview))
        reload_button.triggered.connect(self.webview.reload)

        navigation_bar.addAction(back_button)
        navigation_bar.addAction(next_button)
        navigation_bar.addAction(add_button)
        navigation_bar.addAction(reload_button)

        self.urlbar = QLineEdit()

        self.urlbar.returnPressed.connect(self.navigate_to_url)

        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.urlbar)

        self.webview.urlChanged.connect(self.renew_urlbar)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme('http')
        self.webview.setUrl(q)

    def renew_urlbar(self, q):

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def create_tab(self, webview):
        self.tab = QWidget()
        title = self.browser.page().title()
        self.tabWidget.addTab(self.tab, title)
        self.tabWidget.setCurrentWidget(self.tab)

        self.Layout = QHBoxLayout(self.tab)
        self.Layout.setContentsMargins(90, 0, 0, 0)
        self.Layout.addWidget(webview)

    def update_title(self):
        title = self.browser.page().title()

    def downloadDirectory(self, WebEngineDownloadItem):
        self.setDownloadDirectory("ClRB\download")
        self.setDownloadFileName("heheheh")
        self.isSavePageDownload()

    def close_Tab(self, index):
        if self.tabWidget.count() > 1:
            self.tabWidget.removeTab(index)
        else:
            self.close()


class WebEngineView(QWebEngineView):

    def __init__(self, mainwindow, parent=None):
        super(WebEngineView, self).__init__(parent)
        self.mainwindow = mainwindow

    def createWindow(self, QWebEnginePage_WebWindowType):
        new_webview = WebEngineView(self.mainwindow)
        self.mainwindow.create_tab(new_webview)
        return new_webview


class download(QWebEngineDownloadItem):
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = MainWindow()
    browser.show()
    sys.exit(app.exec_())
