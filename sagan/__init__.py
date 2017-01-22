import smbus
from .baro import Barometer
from .temperature import TemperatureSensor
from .imu import Accelerometer, Magnetometer, Gyroscope
from .rgb_ir import RgbIrSensor
from .uva import UvaSensor
from .rtc import RealTimeClock
from .leds import Leds
from .arducam import Camera

bus = smbus.SMBus(1)
barometer = Barometer(bus, 0x76)
bottom_thermometer = TemperatureSensor(bus, 0x48)
top_thermometer = TemperatureSensor(bus, 0x49)
accelerometer = Accelerometer(bus, 0x1D)
magnetometer = Magnetometer(bus, 0x1D)
gyroscope = Gyroscope(bus, 0x6b)
rgb_ir_sensor = RgbIrSensor(bus, 0x52)
uva_sensor = UvaSensor(bus, 0x38)
real_time_clock = RealTimeClock(bus, 0x51)

sensors = [
    barometer,
    bottom_thermometer,
    top_thermometer,
    accelerometer,
    gyroscope,
    rgb_ir_sensor,
    uva_sensor,
    real_time_clock
]

for sensor in sensors:
    sensor.configure({})

for sensor in sensors:
    assert sensor.self_test(), 'Failed to initialise sensor {}'.format(repr(sensor))

leds = Leds()
camera = Camera()

__all__ = (
    'barometer',
    'bottom_thermometer',
    'top_thermometer',
    'accelerometer',
    'gyroscope',
    'magnetometer',
    'rgb_ir_sensor',
    'uva_sensor',
    'real_time_clock',
    'leds',
    'camera'
)
