""" Конфигурация робота """
from RPiPWM import *

"""
    F - Front
    B - Backside
    L - Left
    R - Right
"""
IP = '173.1.0.78'  # IP адрес куда отправляем видео
RPCServerPort = 8000  # порт RPC сервера
RTP_PORT = 5000
PORT = 9000

chanSrvFL = 8  # канал для передней левой сервы
chanSvrFR = 11  # канал для передней правой сервы
chanSrvBL = 9  # канал для задней левой сервы
chanSrvBR = 10  # канал для задней правой сервы
chanSvrCAM = 5  # канал для сервы с камерой

chanRevMotorLB = 15  # каналы моторов, индексы аналогичны сервам
chanRevMotorRB = 14

servoResolutionDeg = -90, 90    # разрешение с центром в нуле
servoResolutionMcs = 800, 2400
rotateAngle = 57.76     # угол в градусах, на который надо повернуть сервы, чтобы робот крутился на месте
# для квадратных роботов это 45 градусов

SvrFL = Servo270(chanSrvFL)  # передняя левая
SvrFR = Servo270(chanSvrFR)  # передняя правая
SvrBL = Servo270(chanSrvBL)  # задняя левая
SvrBR = Servo270(chanSrvBR)  # задняя правая

MotorLB = ReverseMotor(chanRevMotorLB)  # моторы, индексы аналогичные
MotorRB = ReverseMotor(chanRevMotorRB)


def servoScale(value):  # рескейлим серву, как нам нужно
    degRange = (servoResolutionDeg[1] - servoResolutionDeg[0])
    mskRange = (servoResolutionMcs[1] - servoResolutionMcs[0])
    result = ((value - servoResolutionDeg[0])/degRange) * mskRange + servoResolutionMcs[0]
    if result > servoResolutionMcs[1]:
        return servoResolutionMcs[1]
    elif result < servoResolutionMcs[0]:
        return servoResolutionMcs[0]
    else:
        return int(result)


def rotate(speed):
    """ поворот на месте, speed - скорость поворота """
    SvrFL.SetMcs(servoScale(rotateAngle))
    SvrFR.SetMcs(servoScale(-rotateAngle))
    SvrBL.SetMcs(servoScale(-rotateAngle))
    SvrBR.SetMcs(servoScale(rotateAngle))
    MotorRB.SetValue(speed)
    MotorLB.SetValue(speed)
    return True


def turnAll(scale):
    """ поворот всех серв на один угол"""
    result = servoScale(90 * scale)
    SvrFL.SetMcs(result)
    SvrFR.SetMcs(result)
    SvrBL.SetMcs(result)
    SvrBR.SetMcs(result)
    return True


def turnForward(scale):
    """ поворот передней части робота """
    SvrBR.SetMcs(servoScale(0))
    SvrBL.SetMcs(servoScale(0))
    SvrFL.SetMcs(servoScale(90 * scale))
    SvrFR.SetMcs(servoScale(90 * scale))
    return True


def move(speed):
    """ движение вперед/назад """
    SvrBR.SetMcs(servoScale(0))
    SvrBL.SetMcs(servoScale(0))
    MotorLB.SetValue(speed)
    MotorRB.SetValue(-speed)
    return True
