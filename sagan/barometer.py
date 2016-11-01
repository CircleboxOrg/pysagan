from .i2c import I2cDevice


class Barometer(I2cDevice):
    """
    Interface for BME280 pressure and humidity
    """

    def measure(self):
        pass

    def test(self):
        self.read()