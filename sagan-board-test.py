from smbus import SMBus
from sagan.baro import Barometer
from sagan.temperature import TemperatureSensor
from sagan.imu import Accelerometer, Magnetometer, Gyroscope
from sagan.rgb_ir import RgbIrSensor
from sagan.uva import UvaSensor
from sagan.rtc import RealTimeClock
from sagan.leds import Leds
from time import sleep

bus = SMBus(1)
barometer = Barometer(bus, 0x76)
bottom_temperature = TemperatureSensor(bus, 0x48)
top_temperature = TemperatureSensor(bus, 0x49)
acc_mag = Accelerometer(bus, 0x1D)
mag = Magnetometer(bus, 0x1D)
gyro = Gyroscope(bus, 0x6b)
rgb_ir = RgbIrSensor(bus, 0x52)
uva = UvaSensor(bus, 0x38)
rtc = RealTimeClock(bus, 0x51)

sensors = [barometer, bottom_temperature, top_temperature, acc_mag, gyro, rgb_ir, uva, rtc]

print(all(sensor.self_test() for sensor in sensors))

for sensor in sensors:
    sensor.configure({})

for sensor in sensors:
    print(sensor.measure())

leds = Leds()

leds.set_led1('on')
leds.set_led2('on')
leds.set_red('on')
leds.set_green('on')
leds.set_blue('on')
sleep(1)
leds.set_led1('off')
leds.set_led2('off')
leds.set_red('off')
leds.set_green('off')
leds.set_blue('off')
