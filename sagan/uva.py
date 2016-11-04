from .i2c import I2cDevice


class UvaSensor(I2cDevice):
    def self_test(self) -> bool:
        # There is nothing to do here, only readable registers are the output data
        return True

    def configure(self, args: dict) -> None:
        self.write(0x70, [0x60])

    def measure(self):
        # scale from sensor is 5 uW / cm^2  / encoder count.
        msb = self.read(0x73, 1)[0]
        lsb = self.read(0x71, 1)[0]
        return ((msb << 8) | lsb) * 5e-6
