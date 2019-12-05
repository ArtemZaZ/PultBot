import threading


class FrameHandler(threading.Thread):
    def __init__(self, stream, callback):
        super(FrameHandler, self).__init__(daemon=True)
        self.rpiCamStream = stream
        self._callback = callback
        self._frame = None
        self._stopped = threading.Event()  # событие для остановки потока
        self._newFrameEvent = threading.Event()  # событие для контроля поступления кадров

    def run(self):
        print('Frame handler started')
        while not self._stopped.is_set():  # пока мы живём
            self.rpiCamStream.frameRequest()  # отправил запрос на новый кадр
            self._newFrameEvent.wait()  # ждем появления нового кадра
            self._callback(*self._frame)
            self._newFrameEvent.clear()  # сбрасываем событие
        print('Frame handler stopped')

    def stop(self):  # остановка потока
        self._stopped.set()
        if not self._newFrameEvent.is_set():  # если кадр не обрабатывается
            self._frame = None
            self._newFrameEvent.set()
        self.join()

    def setFrame(self, *args):  # задание нового кадра для обработки
        if not self._newFrameEvent.is_set():  # если обработчик готов принять новый кадр
            self._frame = args
            self._newFrameEvent.set()  # задали событие
        return self._newFrameEvent.is_set()
