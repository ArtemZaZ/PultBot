""" Модуль описывающий управление роботом """
import threading
import time
from pult import config
from pult import socketrobot
from pynput import keyboard


def remapScale(scale):
    """ защита от дурака ограничивает значение scale до диапазона (-1; 1) """
    return min(max(-1.0, scale), 1.0)


class Control(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, daemon=True)
        self.robot = socketrobot.SocketRobot()
        self._joystick = None
        self._keyboard = None
        self._cameraPos = False  # позиция камеры
        self._autoPos = False  # позиция автономки
        self._moveScale = 0.0   # данные о движении робота
        self._turnScale = 0.0
        self._rotateScale = 0.0
        self._manipulatorScaleAxis = [0.0, 0.0, 0.0, 0.0, 0.0]  # позиция манипулятора
        self._manipulatorMoveStep = 0.01     # шаг движения манипулятора
        self._selectedAxis = 1  # выбранная ось поворота манипулятора
        self.__exit = False

    def setJoystick(self, joystick):  # устанавливаем джойстик, которым будем управлять
        self._joystick = joystick
        self._connectJoystickHandlers()

    def fromKeyboard(self):
        self._connectKeyboardHandlers()

    def _connectJoystickHandlers(self):  # привязка обработчиков кнопок
        def addSpeed(w):
            if w:
                self.robot.motorSpeed += config.SPEED_CHANGE_STEP  # прибавляем скорость

        def subSpeed(w):
            if w:
                self.robot.motorSpeed -= config.SPEED_CHANGE_STEP  # уменьшаем скорость

        def rotateCamera(w):
            if w:
                self._cameraPos = not self._cameraPos
                if self._cameraPos:
                    self.robot.setCamera(0.4)
                else:
                    self.robot.setCamera(0.0)
                self.robot.sendPackage()

        self._joystick.onButtonClick(config.ADD_SPEED_BUTTON, addSpeed)
        self._joystick.onButtonClick(config.SUB_SPEED_BUTTON, subSpeed)
        self._joystick.onButtonClick(config.ROTATE_CAMERA_BUTTON, rotateCamera)

    def _connectKeyboardHandlers(self):  # привязка обработчиков кнопок клавиатуры
        def onPress(key):
            try:
                if key.char == 'w':
                    self._moveScale = 1.0
                elif key.char == 's':
                    self._moveScale = -1.0
                if key.char == 'a':
                    self._turnScale = -0.5
                elif key.char == 'd':
                    self._turnScale = 0.5
                if key.char == 'u':
                    self._rotateScale = -1.0
                elif key.char == 'i':
                    self._rotateScale = 1.0
                # вращаем выбранную ось манипулятора
                if key.char == 'q':
                    self._manipulatorScaleAxis[self._selectedAxis - 1] = remapScale(
                        self._manipulatorScaleAxis[self._selectedAxis - 1] - self._manipulatorMoveStep)
                    self.robot.moveManipulator(*self._manipulatorScaleAxis)
                elif key.char == 'e':
                    self._manipulatorScaleAxis[self._selectedAxis - 1] = remapScale(
                        self._manipulatorScaleAxis[self._selectedAxis - 1] + self._manipulatorMoveStep)
                    self.robot.moveManipulator(*self._manipulatorScaleAxis)
            except AttributeError:
                pass

        def onRelease(key):
            try:
                if (key.char == 'w') or (key.char == 's'):
                    self._moveScale = 0.0
                if (key.char == 'a') or (key.char == 'd'):
                    self._turnScale = 0.0
                if (key.char == 'u') or (key.char == 'i'):
                    self._rotateScale = 0.0
                # выбираем ось манипулятора
                if key.char == '1':
                    self._selectedAxis = 1
                if key.char == '2':
                    self._selectedAxis = 2
                if key.char == '3':
                    self._selectedAxis = 3
                if key.char == '4':
                    self._selectedAxis = 4
                if key.char == '5':
                    self._selectedAxis = 5

                if key.char == 'c':
                    if self._cameraPos:
                        self.robot.setCamera(-0.5)
                    else:
                        self.robot.setCamera(0.4)
                    self._cameraPos = not self._cameraPos
                    self.robot.sendPackage()

                if key.char == 'v':
                    if not self._autoPos:
                        self.robot.setAuto(True)
                    else:
                        self.robot.setAuto(False)
                    self._autoPos = not self._autoPos
                    self.robot.sendPackage()
                # изменяем скорость робота
                if key.char == 'z':
                    self.robot.motorSpeed -= config.SPEED_CHANGE_STEP
                elif key.char == 'x':
                    self.robot.motorSpeed += config.SPEED_CHANGE_STEP

            except AttributeError:
                pass

        self._keyboard = keyboard.Listener(on_press=onPress, on_release=onRelease)
        self._keyboard.start()

    def exit(self):
        self.__exit = True
        self.robot.disconnect()

    def run(self):
        while not self.__exit:
            try:
                if self.robot.exist and (self._joystick is not None):  # если клиент и джойстик созданы
                    pass  # тут можно сделать управление с джойстика
                elif self.robot.exist and (self._keyboard is not None):  # если клиент и клавиатура созданы:
                    if self._rotateScale == 0.0:    # если нет поворота на месте
                        self.robot.rotate(self._rotateScale)
                        self.robot.move(self._moveScale)
                        self.robot.turnForward(self._turnScale)
                    else:
                        self.robot.rotate(self._rotateScale)
                    self.robot.sendPackage()
                else:
                    time.sleep(3)
            except Exception as e:
                print("Ошибка управления: " + str(e))
            time.sleep(config.SEND_DELAY)
