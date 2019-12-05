#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Сервер, установленный на малине """
from bot import config
from bot.control import Control
from bot import rpicam
import time

rpiCamStreamer = rpicam.RPiCamStreamer(config.VIDEO_FORMAT, config.VIDEO_RESOLUTION, config.VIDEO_FRAMERATE)
rpiCamStreamer.setPort(config.RTP_PORT)
rpiCamStreamer.setHost(config.IP)
rpiCamStreamer.setRotation(180)

control = Control()

control.connectToEvent(config.turnForward, "turnForward")
control.connectToEvent(config.turnAll, "turnAll")
control.connectToEvent(config.rotate, "rotate")
control.connectToEvent(config.move, "move")
control.connectToEvent(config.setCamera, "setCamera")
control.connectToEvent(config.turnFirstAxisArg, "turnFirstAxisArg")
control.connectToEvent(config.turnSecondAxisArg, "turnSecondAxisArg")
control.connectToEvent(config.turnThirdAxisArg, "turnThirdAxisArg")
control.connectToEvent(config.turnFourthAxisArg, "turnFourthAxisArg")
control.connectToEvent(config.turnFifthAxisArg, "turnFifthAxisArg")
control.connectToEvent(config.setLight, "setLight")

rpiCamStreamer.start()  # запускаем трансляцию
config.initializeAll()

try:
    control.connect('', config.PORT)
except Exception as e:
    raise ConnectionError("Не удалось подключиться к ", (config.IP, config.PORT), str(e))

while True:     # бесконечный цикл
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        control.disconnect()
        break
