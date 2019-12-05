import socket
import struct
from queue import Queue
import threading
import time


class Sender(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self, daemon=True)
        self._connected = False
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._ip = ip
        self._port = port
        self._queue = Queue()
        self._exit = False
        self._packageFormat = 'ffff'

    def connect(self):
        if not self._connected:
            self._sock.connect((self._ip, self._port))
            self._connected = True
            self.start()

    def disconnect(self):
        self._sock.close()
        self._connected = False

    def sendPackage(self, package):
        self._queue.put(package)

    def pack(self, *args):
        return struct.Struct(self._packageFormat).pack(*args)

    def run(self):
        while not self._exit:
            self._sock.send(self._queue.get())
            time.sleep(0.01)

    @property
    def packageFormat(self):
        return self._packageFormat

    @packageFormat.setter
    def packageFormat(self, format):
        self._packageFormat = format
