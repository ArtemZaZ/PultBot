import time

import cv2

from pult import GstCV
from pult import control
from pult import config
import pyzbar.pyzbar as pyzbar

con = control.Control()
con.fromKeyboard()

try:
    con.robot.connect(config.IP, config.PORT)
except Exception as e:
    raise ConnectionError("Не удалось подключиться к ", config.IP, str(e))


qrdata = None


def printQR(frame):
    global qrdata
    decodedObjects = pyzbar.decode(frame)
    if decodedObjects != []:
        for obj in decodedObjects:
            data = obj.data.decode("UTF-8")
            if data != '':
                if qrdata != data:
                    qrdata = data
                    print("QR CODE: ", data)

con.start()
camera = GstCV.CVGstreamer(config.IP, 5000, 5001, 5005, toAVS=False, codec="JPEG")
camera.start()

WIDTH, HEIGHT = (640, 360)
SENSIVITY = 80     # чувствительность автономки
INTENSIVITY = 0   # порог интенсивности
r = int(WIDTH * 1.3 / 6 + 0), int(HEIGHT * 1 / 5 + 0), int(WIDTH * 3.25 / 6 + 0), int(HEIGHT * 4 / 5 - 20)  # прямоугольник, выделяемый в кадре для OpenCV: x, y, width, height


while True:     # бесконечный цикл
    try:

        if camera.cvImage is not None:
            printQR(camera.cvImage)
            frame = camera.cvImage[r[1]:(r[1] + r[3]), r[0]:(r[0] + r[2])]  # r - прямоугольник: x, y, width, height
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            intensivity = int(gray.mean())
            if intensivity < INTENSIVITY:
                ret, binary = cv2.threshold(gray, SENSIVITY, 255,
                                            cv2.THRESH_BINARY)  # если инверсная инвертируем картинку
                print("Inverse")
            else:
                ret, binary = cv2.threshold(gray, SENSIVITY, 255,
                                            cv2.THRESH_BINARY_INV)  # переводим в ьинарное изображение
            cont_img, contours, hierarchy = cv2.findContours(binary, 1, cv2.CHAIN_APPROX_NONE)
            cx, cy = 0, 0
            if len(contours) > 0:  # если нашли контур
                c = max(contours, key=cv2.contourArea)  # ищем максимальный контур
                M = cv2.moments(c)  # получаем массив с координатами
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])  # координата центра по х
                    cy = int(M['m01'] / M['m00'])  # координата центра по у
                cv2.line(frame, (cx, 0), (cx, r[3]), (255, 0, 0), 1)  # рисуем линни
                cv2.line(frame, (0, cy), (r[2], cy), (255, 0, 0), 1)
                cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)  # рисуем контур
                diff = cx / (r[2] / 2) - 1
            else:  # если не нашли контур
                print("I don't see the line")
            cv2.imshow("YES", frame)
            cv2.imshow("NONE", camera.cvImage)
            cv2.imshow("bin", binary)
            cv2.imshow("gray", gray)
            cv2.waitKey(1)
        time.sleep(0.05)

    except KeyboardInterrupt:
        con.exit()
        break

