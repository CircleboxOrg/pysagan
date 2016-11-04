from .i2c import I2cDevice


class RgbIrSensor(I2cDevice):
    def self_test(self) -> bool:
        id = self.read(0x06, 1)[0]
        return id == 0xB2

    def configure(self, args: dict) -> None:
        # set light sensor enabled, colour sensing mode.
        self.pack_and_write(0x00, 'B', 0b00000110)
        super().configure(args)

    def measure(self):
        colour_data = self.read_and_unpack(0x0A, '<BHBHBHBH')
        ir = (colour_data[1] << 16) | colour_data[0]
        red = (colour_data[3] << 16) | colour_data[2]
        green = (colour_data[5] << 16) | colour_data[4]
        blue = (colour_data[7] << 16) | colour_data[6]
        return red, green, blue, ir
