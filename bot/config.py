""" Конфигурация робота """
import cv2

from bot.RPiPWM import *
from bot import rpicam
from utility.linewalk import lineOffset
import numpy as np

"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""
IP = "192.168.42.100"
PORT = 8004
RTP_PORT = 5000

VIDEO_FORMAT = rpicam.VIDEO_MJPEG  # поток MJPEG
VIDEO_RESOLUTION = (640, 360)
VIDEO_FRAMERATE = 20
WIDTH, HEIGHT = VIDEO_RESOLUTION

# прямоугольник, который обрезает кадр у автономки
VIDEO_AUTO_SLICE_RECT = int(WIDTH * 1.3 / 6 + 0), int(HEIGHT * 1 / 5 + 0), int(WIDTH * 3.25 / 6 + 0), int(HEIGHT * 4 / 5 - 20)  # прямоугольник, выделяемый в кадре для OpenCV: x, y, width, height
SENSIVITY = 80  # эти параметры задаются с ПК
INTENSIVITY = 0  # порог интенсивности
AUTO = False
AUTO_SPEED = 20


chanLight = 0  # канал фар
chanSrvFL = 1  # канал для передней левой сервы
chanSrvFR = 2  # канал для передней правой сервы
chanSrvBL = 3  # канал для задней левой сервы
chanSrvBR = 4  # канал для задней правой сервы
chanSrvCAM = 5  # канал для сервы с камерой

chanSrvM1A = 6  # канал 1 оси манипулятора
chanSrvM2A = 7  # канал 2 оси манипулятора
chanSrvM3A = 8  # канал 3 оси манипулятора
chanSrvM4A = 9  # канал 4 оси манипулятора
chanSrvM5A = 10  # канал 5 оси манипулятора

chanMotorL = 14  # каналы моторов, индексы аналогичны сервам
chanMotorR = 15

srvResolutionMcs = (800, 2200)  # центр в 1500
mtrResolutionMcs = (800, 2200)  # разрещение скоростей мотора в мкс
mtrBias = 80  # смещение скорости мотора в мкс
srvFLOffset = 140
srvFROffset = 100
srvBLOffset = 120
srvBROffset = 160

rotateAngleScale = 0.643  # угол в mcs, на который надо повернуть сервы, чтобы робот крутился\
#  на месте (тут примено 57 градусов) для квадратных роботов это 45 градусов (примерно 1850 mcs)

Light = Servo90(chanLight)  # фары
SrvFL = Servo270(chanSrvFL)  # передняя левая
SrvFR = Servo270(chanSrvFR)  # передняя правая
SrvBL = Servo270(chanSrvBL)  # задняя левая
SrvBR = Servo270(chanSrvBR)  # задняя правая
SrvCAM = Servo90(chanSrvCAM)  # серва камеры

SrvM1A = Servo270(chanSrvM1A)  # сервы манипулятора
SrvM2A = Servo270(chanSrvM2A)
SrvM3A = Servo270(chanSrvM3A)
SrvM4A = Servo270(chanSrvM4A)
SrvM5A = Servo270(chanSrvM5A)

MotorL = ReverseMotor(chanMotorL)  # моторы, индексы аналогичные
MotorR = ReverseMotor(chanMotorR)


def getMcsBySpeed(speed):
    """ получаем значение мкс из значения скорости (-100, 100) """
    scale = min(max(-1.0, speed / 100), 1.0)  # проверяем еще раз значение scale
    speed = int(((scale + 1) / 2) * (mtrResolutionMcs[1] - mtrResolutionMcs[0]) + mtrResolutionMcs[0])
    return int(speed) + mtrBias


def getMcsByScale(scale):
    """ получаем нужные значения мкс(srvResolutionMcs[0], srvResolutionMcs[1]) из значения scale (-1:1) """
    scale = min(max(-1.0, scale), 1.0)  # проверяем еще раз значение scale
    return int(((scale + 1) / 2) * (srvResolutionMcs[1] - srvResolutionMcs[0]) + srvResolutionMcs[0])


def turnForward(scale):
    SrvFL.setMcs(getMcsByScale(scale) + srvFLOffset)
    SrvFR.setMcs(getMcsByScale(scale) + srvFROffset)
    SrvBR.setMcs(getMcsByScale(-scale) + srvBROffset)
    SrvBL.setMcs(getMcsByScale(-scale) + srvBLOffset)


def move(speed):
    MotorL.setMcs(getMcsBySpeed(speed))
    MotorR.setMcs(getMcsBySpeed(speed))


def rotate(speed):
    if abs(speed) < 10:  # если скорость меньше 10, то возвращаемся из состояния поворота на месте
        SrvFL.setMcs(getMcsByScale(0) + srvFLOffset)
        SrvFR.setMcs(getMcsByScale(0) + srvFROffset)
        SrvBR.setMcs(getMcsByScale(0) + srvBROffset)
        SrvBL.setMcs(getMcsByScale(0) + srvBLOffset)
        MotorL.setMcs(getMcsBySpeed(0))
        MotorR.setMcs(getMcsBySpeed(0))
    else:
        SrvFL.setMcs(getMcsByScale(rotateAngleScale) + srvFLOffset)
        SrvFR.setMcs(getMcsByScale(-rotateAngleScale) + srvFROffset)
        SrvBR.setMcs(getMcsByScale(rotateAngleScale) + srvBROffset)
        SrvBL.setMcs(getMcsByScale(-rotateAngleScale) + srvBLOffset)
        MotorL.setMcs(getMcsBySpeed(speed))
        MotorR.setMcs(getMcsBySpeed(-speed))


def turnAll(scale):
    pass


def setCamera(scale):
    SrvCAM.setMcs(getMcsByScale(scale))


def turnFirstAxisArg(scale):
    SrvM1A.setMcs(getMcsByScale(scale))


def turnSecondAxisArg(scale):
    SrvM2A.setMcs(getMcsByScale(scale))


def turnThirdAxisArg(scale):
    SrvM3A.setMcs(getMcsByScale(scale))


def turnFourthAxisArg(scale):
    SrvM4A.setMcs(getMcsByScale(scale))


def turnFifthAxisArg(scale):
    SrvM5A.setMcs(getMcsByScale(scale))


def setAuto(pos):
    global AUTO
    AUTO = pos
    if AUTO is False:
        move(0)


def setSensivity(sens):
    global SENSIVITY
    SENSIVITY = sens


def setIntensivity(intens):
    global INTENSIVITY
    INTENSIVITY = intens


def onFrameRequest(*args):
    global AUTO
    frame, w, h = args

    while not AUTO:  # пока не включена автономка - спим
        time.sleep(0.2)

    if frame is not None:
        r = VIDEO_AUTO_SLICE_RECT
        frameSlice = frame[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]
        gray = cv2.cvtColor(frameSlice, cv2.COLOR_BGR2GRAY)  # делаем ч/б
        res = lineOffset(INTENSIVITY, SENSIVITY, gray)
        if res is not None:
            cx, cy = res
            turnForward(cx)
            move(AUTO_SPEED)
    time.sleep(0.05)  # в коде работы камеры есть утечка памяти, это значение де делайте слишком маленьким


def initializeAll():
    MotorL.setMcs(getMcsBySpeed(0))
    MotorR.setMcs(getMcsBySpeed(0))
    SrvFL.setMcs(getMcsByScale(0) + srvFLOffset)
    SrvFR.setMcs(getMcsByScale(0) + srvFROffset)
    SrvBR.setMcs(getMcsByScale(0) + srvBROffset)
    SrvBL.setMcs(getMcsByScale(0) + srvBLOffset)
    SrvCAM.setMcs(getMcsByScale(-0.4))
    time.sleep(0.5)
    SrvM1A.setMcs(getMcsByScale(0))
    time.sleep(0.5)
    SrvM2A.setMcs(getMcsByScale(0))
    time.sleep(0.5)
    SrvM3A.setMcs(getMcsByScale(0))
    time.sleep(0.5)
    SrvM4A.setMcs(getMcsByScale(0))
    time.sleep(0.5)
    SrvM5A.setMcs(getMcsByScale(0))
    time.sleep(0.5)
