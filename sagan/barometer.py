from .i2c import I2cDevice


class Barometer(I2cDevice):
    """
    Interface for BME280 pressure and humidity
    """
    def measure(self):
        frame = self.read(0xF7, 0xFE - 0xF7)
        return frame

    def test(self):
        id = self.read(0xD0, 1)[0]
        return id == 0x60
