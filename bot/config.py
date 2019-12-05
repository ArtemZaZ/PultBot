""" Конфигурация робота """
from bot.RPiPWM import *
from bot import rpicam
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
mtrBias = 80    # смещение скорости мотора в мкс
srvFLOffset = 140
srvFROffset = 100
srvBLOffset = 120
srvBROffset = 160

rotateAngleScale = 0.643     # угол в mcs, на который надо повернуть сервы, чтобы робот крутился\
#  на месте (тут примено 57 градусов) для квадратных роботов это 45 градусов (примерно 1850 mcs)

Light = Servo90(chanLight)  # фары
SrvFL = Servo270(chanSrvFL)  # передняя левая
SrvFR = Servo270(chanSrvFR)  # передняя правая
SrvBL = Servo270(chanSrvBL)  # задняя левая
SrvBR = Servo270(chanSrvBR)  # задняя правая
SrvCAM = Servo90(chanSrvCAM)    # серва камеры

SrvM1A = Servo270(chanSrvM1A)   # сервы манипулятора
SrvM2A = Servo270(chanSrvM2A)
SrvM3A = Servo270(chanSrvM3A)
SrvM4A = Servo270(chanSrvM4A)
SrvM5A = Servo270(chanSrvM5A)

MotorL = ReverseMotor(chanMotorL)  # моторы, индексы аналогичные
MotorR = ReverseMotor(chanMotorR)


def getMcsBySpeed(speed):
    """ получаем значение мкс из значения скорости (-100, 100) """
    scale = min(max(-1.0, speed/100), 1.0)  # проверяем еще раз значение scale
    speed = int(((scale + 1)/2) * (mtrResolutionMcs[1] - mtrResolutionMcs[0]) + mtrResolutionMcs[0])
    return int(speed) + mtrBias


def getMcsByScale(scale):
    """ получаем нужные значения мкс(srvResolutionMcs[0], srvResolutionMcs[1]) из значения scale (-1:1) """
    scale = min(max(-1.0, scale), 1.0)  # проверяем еще раз значение scale
    return int(((scale + 1)/2) * (srvResolutionMcs[1] - srvResolutionMcs[0]) + srvResolutionMcs[0])


def turnForward(scale):
    SrvFL.setMcs(getMcsByScale(scale) + srvFLOffset)
    SrvFR.setMcs(getMcsByScale(scale) + srvFROffset)
    SrvBR.setMcs(getMcsByScale(-scale) + srvBROffset)
    SrvBL.setMcs(getMcsByScale(-scale) + srvBLOffset)


def move(speed):
    MotorL.setMcs(getMcsBySpeed(speed))
    MotorR.setMcs(getMcsBySpeed(speed))


def rotate(speed):
    if abs(speed) < 10:     # если скорость меньше 10, то возвращаемся из состояния поворота на месте
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


def setLight(pos):
    Light.setMcs(1500)
    time.sleep(0.5)
    Light.setMcs(800)


def initializeAll():
    MotorL.setMcs(getMcsBySpeed(0))
    MotorR.setMcs(getMcsBySpeed(0))
    SrvFL.setMcs(getMcsByScale(0) + srvFLOffset)
    SrvFR.setMcs(getMcsByScale(0) + srvFROffset)
    SrvBR.setMcs(getMcsByScale(0) + srvBROffset)
    SrvBL.setMcs(getMcsByScale(0) + srvBLOffset)
    time.sleep(1)
    SrvM1A.setMcs(getMcsByScale(0))
    time.sleep(1)
    SrvM2A.setMcs(getMcsByScale(0))
    time.sleep(1)
    SrvM3A.setMcs(getMcsByScale(0))
    time.sleep(1)
    SrvM4A.setMcs(getMcsByScale(0))
    time.sleep(1)
    SrvM5A.setMcs(getMcsByScale(0))
    time.sleep(1)
