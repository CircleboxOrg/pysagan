import time

from .i2c import I2cDevice

BME280_REGISTER_T1 = 0x88  # Trimming parameter registers
BME280_REGISTER_T2 = 0x8A
BME280_REGISTER_T3 = 0x8C

BME280_REGISTER_P1 = 0x8E
BME280_REGISTER_P2 = 0x90
BME280_REGISTER_P3 = 0x92
BME280_REGISTER_P4 = 0x94
BME280_REGISTER_P5 = 0x96
BME280_REGISTER_P6 = 0x98
BME280_REGISTER_P7 = 0x9A
BME280_REGISTER_P8 = 0x9C
BME280_REGISTER_P9 = 0x9E

BME280_REGISTER_H1 = 0xA1
BME280_REGISTER_H2 = 0xE1
BME280_REGISTER_H3 = 0xE3
BME280_REGISTER_H4 = 0xE4
BME280_REGISTER_H5 = 0xE5
BME280_REGISTER_H6 = 0xE6
BME280_REGISTER_H7 = 0xE7

BME280_REGISTER_CHIPID = 0xD0
BME280_REGISTER_VERSION = 0xD1
BME280_REGISTER_SOFTRESET = 0xE0

BME280_REGISTER_CONTROL_HUM = 0xF2
BME280_REGISTER_CONTROL = 0xF4
BME280_REGISTER_CONFIG = 0xF5
BME280_REGISTER_PRESSURE_DATA = 0xF7
BME280_REGISTER_TEMP_DATA = 0xFA
BME280_REGISTER_HUMIDITY_DATA = 0xFD


class Barometer(I2cDevice):
    data_frame = '<HBHBH'
    parameters_frame_1 = '<HhhHhhhhhhhhB'
    parameters_frame_2 = '<hBhhb'
    mode = 0b1  # 'Forced' mode
    pressure_oversample = 1
    temperature_oversample = 1
    humidity_oversample = 1

    temperature_parameters = [0] * 3
    pressure_parameters = [0] * 9
    humidity_parameters = [0] * 6

    """
    Interface for BME280 pressure and humidity
    """
    def read_raw_measurements(self):
        # Forced measurement mode
        if self.mode in (0b01, 0b10):
            self.configure()
        # TODO: calculate appropriate sleep time, this is in the data sheet
        time.sleep(0.500)
        return self.read_and_unpack(0xF7, self.data_frame)

    def measure(self):
        p_raw, px_raw, t_raw, tx_raw, h_raw = self.read_raw_measurements()
        T1 = self.temperature_parameters[0]
        T2 = self.temperature_parameters[1]
        T3 = self.temperature_parameters[2]
        var1 = (t_raw / 16384.0 - T1 / 1024.0) * float(T2)
        var2 = ((t_raw / 131072.0 - T1 / 8192.0) * (t_raw / 131072.0 - T1 / 8192.0)) * float(T3)
        # self.t_fine = int(var1 + var2)
        temp = (var1 + var2) / 5120.0
        return temp + 273.15

    def test(self):
        id, = self.read_and_unpack(BME280_REGISTER_CHIPID, 'B')
        return id == 0x60

    def configure(self):
        ctrl_meas = (self.temperature_oversample << 5) | (self.pressure_oversample << 2) | self.mode
        ctrl_hum = self.humidity_oversample & 0b00000111
        self.pack_and_write(0xF2, 'B', ctrl_hum)
        self.pack_and_write(0xF4, 'B', ctrl_meas)

    def read_parameters(self):
        frame_1 = self.read_and_unpack(0x88, self.parameters_frame_1)
        self.temperature_parameters = frame_1[0:3]
        self.pressure_parameters = frame_1[3:12]
