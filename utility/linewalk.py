import cv2


def lineOffset(intensivity, sensivity, frame):  # смещение линии на кадре
    shape = frame.shape
    shape = shape[1], shape[0]
    intens = int(frame.mean())  # получаем среднее значение
    if intens < intensivity:  # условие интесивности
        ret, binary = cv2.threshold(frame, sensivity, 255,
                                    cv2.THRESH_BINARY)  # если инверсная инвертируем картинку
        print("Inverse")

    else:
        ret, binary = cv2.threshold(frame, sensivity, 255,
                                    cv2.THRESH_BINARY_INV)  # переводим в ьинарное изображение

    # Find the contours of the frame
    cont_img, contours, hierarchy = cv2.findContours(binary.copy(), 1,
                                                     cv2.CHAIN_APPROX_NONE)  # получаем список контуров

    # Find the biggest contour (if detected)
    cx, cy = shape[0]/2, shape[1]/2
    if len(contours) > 0:  # если нашли контур
        c = max(contours, key=cv2.contourArea)  # ищем максимальный контур
        M = cv2.moments(c)  # получаем массив с координатами
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])  # координата центра по х
            cy = int(M['m01'] / M['m00'])  # координата центра по у
        #cv2.line(frame, (cx, 0), (cx, shape[1]), (255, 0, 0), 1)  # рисуем линни
        #cv2.line(frame, (0, cy), (shape[0], cy), (255, 0, 0), 1)

        #cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)  # рисуем контур

        diffx = cx/(shape[0]/2) - 1
        diffy = cy/(shape[1]/2) - 1
        return diffx, diffy

    else:  # если не нашли контур
        print("I don't see the line")

    return None

