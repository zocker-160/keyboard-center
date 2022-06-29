#! /usr/bin/env python3

from PyQt5.QtCore import QTextStream, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtNetwork import QLocalSocket, QLocalServer

class QSingleApplication(QApplication):

    onActivate = pyqtSignal()

    def __init__(self, id: str, *argv):
        super().__init__(*argv)

        self.aboutToQuit.connect(self.stopSockets)

        self.id = id
        self.server: QLocalServer = None
        self.dataStream: QTextStream = None

        self.localSocket = QLocalSocket(self)
        self.localSocket.connectToServer(self.id)

        self.isRunning = self.localSocket.waitForConnected()

        if self.isRunning:
            self.dataStream = QTextStream(self.localSocket)
            self.dataStream << "activate"
            self.dataStream.flush()
            self.localSocket.waitForBytesWritten()
        else:
            self.server = QLocalServer(self)
            self.server.listen(self.id)
            self.server.newConnection.connect(self.onNewConnection)

    def onNewConnection(self):
        inSocket = self.server.nextPendingConnection()
        if not inSocket: return

        inStream = QTextStream(inSocket)
        inSocket.readyRead.connect(lambda: self.onReadyRead(inStream))

    def onReadyRead(self, inStream: QTextStream):
        msg = inStream.readAll()

        if msg == "activate":
            print("activate triggered")
            self.onActivate.emit()

    def stopSockets(self):
        self.localSocket.close()    
        if self.server:
            self.server.close()
