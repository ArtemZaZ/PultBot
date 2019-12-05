import time

from pult import control
from pult import config


con = control.Control()
con.fromKeyboard()

try:
    con.robot.connect(config.IP, config.PORT)
except Exception as e:
    raise ConnectionError("Не удалось подключиться к ", config.IP, str(e))

con.start()

while True:     # бесконечный цикл
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        con.exit()
        break

