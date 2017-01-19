from .i2c import I2cDevice

# Addresses
MAG_ADDRESS = 0x1D
ACC_ADDRESS = 0x1D
GYR_ADDRESS = 0x6B

# LSM9DS0 Gyro Registers
WHO_AM_I_G = 0x0F
CTRL_REG1_G = 0x20
CTRL_REG2_G = 0x21
CTRL_REG3_G = 0x22
CTRL_REG4_G = 0x23
CTRL_REG5_G = 0x24
REFERENCE_G = 0x25
STATUS_REG_G = 0x27
OUT_X_L_G = 0x28
OUT_X_H_G = 0x29
OUT_Y_L_G = 0x2A
OUT_Y_H_G = 0x2B
OUT_Z_L_G = 0x2C
OUT_Z_H_G = 0x2D
FIFO_CTRL_REG_G = 0x2E
FIFO_SRC_REG_G = 0x2F
INT1_CFG_G = 0x30
INT1_SRC_G = 0x31
INT1_THS_XH_G = 0x32
INT1_THS_XL_G = 0x33
INT1_THS_YH_G = 0x34
INT1_THS_YL_G = 0x35
INT1_THS_ZH_G = 0x36
INT1_THS_ZL_G = 0x37
INT1_DURATION_G = 0x38

# LSM9DS0 Accel and Magneto Registers
OUT_TEMP_L_XM = 0x05
OUT_TEMP_H_XM = 0x06
STATUS_REG_M = 0x07
OUT_X_L_M = 0x08
OUT_X_H_M = 0x09
OUT_Y_L_M = 0x0A
OUT_Y_H_M = 0x0B
OUT_Z_L_M = 0x0C
OUT_Z_H_M = 0x0D
WHO_AM_I_XM = 0x0F
INT_CTRL_REG_M = 0x12
INT_SRC_REG_M = 0x13
INT_THS_L_M = 0x14
INT_THS_H_M = 0x15
OFFSET_X_L_M = 0x16
OFFSET_X_H_M = 0x17
OFFSET_Y_L_M = 0x18
OFFSET_Y_H_M = 0x19
OFFSET_Z_L_M = 0x1A
OFFSET_Z_H_M = 0x1B
REFERENCE_X = 0x1C
REFERENCE_Y = 0x1D
REFERENCE_Z = 0x1E
CTRL_REG0_XM = 0x1F
CTRL_REG1_XM = 0x20
CTRL_REG2_XM = 0x21
CTRL_REG3_XM = 0x22
CTRL_REG4_XM = 0x23
CTRL_REG5_XM = 0x24
CTRL_REG6_XM = 0x25
CTRL_REG7_XM = 0x26
STATUS_REG_A = 0x27
OUT_X_L_A = 0x28
OUT_X_H_A = 0x29
OUT_Y_L_A = 0x2A
OUT_Y_H_A = 0x2B
OUT_Z_L_A = 0x2C
OUT_Z_H_A = 0x2D
FIFO_CTRL_REG = 0x2E
FIFO_SRC_REG = 0x2F
INT_GEN_1_REG = 0x30
INT_GEN_1_SRC = 0x31
INT_GEN_1_THS = 0x32
INT_GEN_1_DURATION = 0x33
INT_GEN_2_REG = 0x34
INT_GEN_2_SRC = 0x35
INT_GEN_2_THS = 0x36
INT_GEN_2_DURATION = 0x37
CLICK_CFG = 0x38
CLICK_SRC = 0x39
CLICK_THS = 0x3A
TIME_LIMIT = 0x3B
TIME_LATENCY = 0x3C
TIME_WINDOW = 0x3D


class Lsm9ds0I2cDevice(I2cDevice):
    """
    This overrides the read method to toggle the high bit in the register address.
    This is needed for multi-byte reads.
    """
    def read(self, cmd, length):
        cmd |= 0x80
        return super(Lsm9ds0I2cDevice, self).read(cmd, length)


class Accelerometer(Lsm9ds0I2cDevice):
    # These values come from the LSM9DS0 data sheet p13 table3 in the row about sensitivities.
    acceleration_scale = 0.000732 * 9.80665
    magnetometer_scale = 0.00048

    def self_test(self) -> bool:
        id, = self.read_and_unpack(0x0F, 'B')
        return id == 0b01001001

    def configure(self, args: dict) -> None:
        self.write(CTRL_REG1_XM, [0b01100111])
        self.write(CTRL_REG2_XM, [0b00100000])

        # initialise the magnetometer
        self.write(CTRL_REG5_XM, [0b11110000])
        self.write(CTRL_REG6_XM, [0b01100000])
        self.write(CTRL_REG7_XM, [0b00000000])

    def measure(self):
        """
        :return: pair of: acceleration (X, Y, Z triple in m s^-1), magnetic field (X, Y, Z triple in mgauss)
        """
        acc = self.read_and_unpack(0x28, '<hhh')
        mag = self.read_and_unpack(0x08, '<hhh')
        acc = tuple(acc * self.acceleration_scale for acc in acc)
        mag = tuple(mag * self.magnetometer_scale for mag in mag)
        return acc

    @property
    def x(self):
        return self.measure()[0]

    @property
    def y(self):
        return self.measure()[1]

    @property
    def z(self):
        return self.measure()[2]


class Magnetometer(Lsm9ds0I2cDevice):
    # These values come from the LSM9DS0 data sheet p13 table3 in the row about sensitivities.
    acceleration_scale = 0.000732 * 9.80665
    magnetometer_scale = 0.00048

    def self_test(self) -> bool:
        id, = self.read_and_unpack(0x0F, 'B')
        return id == 0b01001001

    def configure(self, args: dict) -> None:
        self.write(CTRL_REG1_XM, [0b01100111])
        self.write(CTRL_REG2_XM, [0b00100000])

        # initialise the magnetometer
        self.write(CTRL_REG5_XM, [0b11110000])
        self.write(CTRL_REG6_XM, [0b01100000])
        self.write(CTRL_REG7_XM, [0b00000000])

    def measure(self):
        """
        :return: pair of: acceleration (X, Y, Z triple in m s^-1), magnetic field (X, Y, Z triple in mgauss)
        """
        acc = self.read_and_unpack(0x28, '<hhh')
        mag = self.read_and_unpack(0x08, '<hhh')
        acc = tuple(acc * self.acceleration_scale for acc in acc)
        mag = tuple(mag * self.magnetometer_scale for mag in mag)
        return mag

    @property
    def x(self):
        return self.measure()[0]

    @property
    def y(self):
        return self.measure()[1]

    @property
    def z(self):
        return self.measure()[2]


class Gyroscope(Lsm9ds0I2cDevice):
    gyroscope_scale = 0.070

    def self_test(self) -> bool:
        id, = self.read_and_unpack(0x0F, 'B')
        return id == 0b11010100

    def configure(self, args: dict):
        # initialise the gyroscope
        self.write(CTRL_REG1_G, [0b00001111])
        self.write(CTRL_REG4_G, [0b00110000])

    def measure(self):
        """
        :return: X, Y, Z triple in degrees per second
        """
        gyro = self.read_and_unpack(0x28, '<hhh')
        gyro = tuple(gyro * self.gyroscope_scale for gyro in gyro)
        return gyro

    @property
    def x(self):
        return self.measure()[0]

    @property
    def y(self):
        return self.measure()[1]

    @property
    def z(self):
        return self.measure()[2]