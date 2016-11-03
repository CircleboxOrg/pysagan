from .i2c import I2cDevice


def _parse_temp_bytes(hi, lo):
    value = ((hi << 8) | lo) >> 5
    if hi & (1 << 7):
        value = - ((~value & ((1 << 11) - 1)) + 1)
    value *= 0.125
    return value


class TemperatureSensor(I2cDevice):
    """
    Interface for LM75B.
    """
    def measure(self):
        temp = self.read(0, 2)
        return _parse_temp_bytes(temp[0], temp[1])

    def self_test(self):
        config = self.read(0x00, 1)[0]
        return config == 0x00
