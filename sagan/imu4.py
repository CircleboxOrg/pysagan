from .i2c import I2cDevice
from .telemetry import Telemetry
from collections import namedtuple
import json

# LSM9DS1 Accel Register
CTRL_REG6_XL = 0x20

# LSM9DS1 Magneto Registers
CTRL_REG1_M = 0x20
CTRL_REG2_M = 0x21
CTRL_REG3_M = 0x22
CTRL_REG4_M = 0x23

# LSM9DS1 Gyro Registers
CTRL_REG1_G = 0x10
CTRL_REG2_G = 0x11
CTRL_REG3_G = 0x12



AccelerometerMeasurement = namedtuple(
    'AccelerometerMeasurement',
    'x y z'
)


GyroscopeMeasurement = namedtuple(
    'GyroscopeMeasurement',
    'x y z'
)


MagnetometerMeasurement = namedtuple(
    'MagnetometerMeasurement',
    'x y z'
)


class Lsm9ds1I2cDevice(I2cDevice):
    """
    This overrides the read method to toggle the high bit in the register address.
    This is needed for multi-byte reads.
    """
    def read(self, cmd, length):
        cmd |= 0x80
        return super(Lsm9ds1I2cDevice, self).read(cmd, length)


class Accelerometer(I2cDevice):
    # This value comes from the LSM9DS1 data sheet pg 12 table3 in the row about sensitivities.
    acceleration_scale = 0.000732 * 9.80665

    def self_test(self):
        id, = self.read_and_unpack(0x0F, 'B')
        return id == 0b01101000
        print("Accelerometer self test - return id = ", id)

    def configure(self, args):

        
        #initialize the accelerometer
        # 119Hz, +/- 16g, bw=50Hz
        self.write(CTRL_REG6_XL, [0b01101000])
        

    def measure(self):
        """
        :return: acceleration (X, Y, Z triple in m s^-2)
        """
        acc = self.read_and_unpack(0x28, '<hhh')
        acc = tuple(acc * self.acceleration_scale for acc in acc)
        result = AccelerometerMeasurement(*acc)
        packet = {
            "x": str(result[0]),
            "y": str(result[1]),
            "z": str(result[2])
        }

        Telemetry.update("acc", packet)
        return result

    @property
    def x(self):
        return self.measure()[0]

    @property
    def y(self):
        return self.measure()[1]

    @property
    def z(self):
        return self.measure()[2]


class Magnetometer(I2cDevice):
    # This value comes from the LSM9DS1 data sheet pg 12 table3 in the row about sensitivities.
    magnetometer_scale = 0.00058

    def self_test(self):
        id, = self.read_and_unpack(0x0F, 'B')
        return id == 0b00111101

    def configure(self, args):
        # initialise the magnetometer
        # ultra-high resolution X&Y, 80Hz rate
        self.write(CTRL_REG1_M, [0b01111100])
        
        # 16 gauss
        self.write(CTRL_REG2_M, [0b01100000])
        
        # continuous conversion
        self.write(CTRL_REG3_M, [0b00000000])
        
        # ultra-high resolution Z
        self.write(CTRL_REG4_M, [0b00001100])

    def measure(self):
        """
        :return: magnetic field (X, Y, Z triple in mgauss)
        """
        mag = self.read_and_unpack(0x28, '<hhh')
        mag = tuple(mag * self.magnetometer_scale for mag in mag)
        result = MagnetometerMeasurement(*mag)

        packet = {
            "x": str(result[0]),
            "y": str(result[1]),
            "z": str(result[2])
        }

        Telemetry.update("mag", packet)

        return result

    @property
    def x(self):
        return self.measure()[0]

    @property
    def y(self):
        return self.measure()[1]

    @property
    def z(self):
        return self.measure()[2]


class Gyroscope(Lsm9ds1I2cDevice):
    # This value comes from the LSM9DS1 data sheet pg 12 table3 in the row about sensitivities.
    gyroscope_scale = 0.070

    def self_test(self):
        id, = self.read_and_unpack(0x0F, 'B')
        return id == 0b01101000

    def configure(self, args):
        # initialise the gyroscope
        self.write(CTRL_REG1_G, [0b01111000]) #2000 dps full scale, 119Hz, 14 cutoff
    
        

    def measure(self):
        """
        :return: X, Y, Z triple in degrees per second
        """
        gyro = self.read_and_unpack(0x18, '<hhh')
        gyro = tuple(gyro * self.gyroscope_scale for gyro in gyro)
        result = GyroscopeMeasurement(*gyro)

        packet = {
            "x": str(result[0]),
            "y": str(result[1]),
            "z": str(result[2])
        }

        Telemetry.update("gyr", packet)
        return result

    @property
    def x(self):
        return self.measure()[0]

    @property
    def y(self):
        return self.measure()[1]

    @property
    def z(self):
        return self.measure()[2]

