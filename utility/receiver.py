import socket
import time
import threading
import struct
from utility import eventmaster


class Receiver(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self, daemon=True)
        self._connected = False
        self._ip = ip
        self._port = port
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn = None
        self.__exit = False
        self._eventDict = {"onReceive": eventmaster.Event("onReceive")}
        self._eventMaster = eventmaster.EventMaster()
        self._eventMaster.append(self._eventDict.get("onReceive"))
        self._eventMaster.start()
        self._packageFormat = None

    def connect(self):
        if not self._connected:
            self._sock.bind((self._ip, self._port))
            self._sock.listen(1)
            self._conn, _ = self._sock.accept()
            self._connected = True
            self.start()

    def disconnect(self):
        self._sock.close()
        self._connected = False

    def connectToEvent(self, foo, toEvent):
        event = self._eventDict.get(toEvent)
        if event:
            event.connect(foo)
        else:
            raise KeyError(toEvent, ": такого события нет")

    def run(self):
        while not self.__exit:
            try:
                data = self._conn.recv(struct.calcsize(self._packageFormat))
                self._eventDict.get("onReceive").push(struct.unpack(self._packageFormat, data))
            except Exception as e:
                print("Проблемы с приемом: " + str(e))
            time.sleep(0.01)

    @property
    def packageFormat(self):
        return self._packageFormat

    @packageFormat.setter
    def packageFormat(self, format):
        self._packageFormat = format