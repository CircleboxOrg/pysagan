import smbus
from .barometer import Barometer
from .temperature import TemperatureSensor
from .imu import Accelerometer, Magnetometer, Gyroscope
from .rgb_ir import RgbIrSensor
from .uva import UvaSensor
from .rtc import RealTimeClock
from .leds import Leds

bus = smbus.SMBus(1)
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

for sensor in sensors:
    sensor.configure({})

leds = Leds()

