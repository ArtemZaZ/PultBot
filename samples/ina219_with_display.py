import time
import board
from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
from PIL import Image       # библиотеки для рисования на дисплее
from PIL import ImageDraw
from PIL import ImageFont
import Adafruit_SSD1306

i2c_bus = board.I2C()

ina219 = INA219(i2c_bus)

# optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage
ina219.bus_adc_resolution = ADCResolution.ADCRES_12BIT_32S
ina219.shunt_adc_resolution = ADCResolution.ADCRES_12BIT_32S
# optional : change voltage range to 16V
ina219.bus_voltage_range = BusVoltageRange.RANGE_16V

# создаем объект для работы с дисплеем (еще возможные варианты - 128_32 и 96_16 - размеры дисплеев в пикселях)
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)
disp.begin()    # запускаем дисплей
disp.clear()    # очищаем буффер изображения

width, height = disp.width, disp.height  # получаем высоту и ширину дисплея

image = Image.new('1', (width, height))     # создаем изображение из библиотеки PIL для вывода на экран
draw = ImageDraw.Draw(image)    # создаем объект, которым будем рисовать
top = -2    # сдвигаем текст вверх на 2 пикселя
x = 0   # сдвигаем весь текст к левому краю
font = ImageFont.load_default()     # загружаем стандартный шрифт

# measure and display loop
while True:
    bus_voltage = ina219.bus_voltage        # voltage on V- (load side)
    shunt_voltage = ina219.shunt_voltage    # voltage between V+ and V- across the shunt
    current = ina219.current                # current in mA

    draw.rectangle((0, 0, width, height), outline=0, fill=0)  # прямоугольник, залитый черным - очищаем дисплей
    draw.text((x, top), "Some interesting info", font=font, fill=255)        # формируем текст
    draw.text((x, top + 8), "Voltage: " + str(bus_voltage) + " V", font=font, fill=255)     # высота строки - 8 пикселей
    draw.text((x, top + 16), "Current: " + str(current/1000) + " A", font=font, fill=255)

    disp.image(image)   # записываем изображение в буффер
    disp.display()      # выводим его на экран

    time.sleep(2)
