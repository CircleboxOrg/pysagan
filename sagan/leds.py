from RPi import GPIO


class Leds:
    led1_pin = 27
    led2_pin = 22
    red_pin = 25
    green_pin = 23
    blue_pin = 24
    on = False
    off = True

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

        # Check that the mode is set correctly
        self.mode = GPIO.getmode()
        if self.mode != 11:
            raise Exception("GPIO Not in BCM mode, try run program as superuser (sudo).")

            # Disable warnings, they are annoying and don't mean anything in this case
        GPIO.setwarnings(False)

        GPIO.setup(self.led1_pin, GPIO.OUT)
        GPIO.setup(self.led2_pin, GPIO.OUT)
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)
        GPIO.setup(self.blue_pin, GPIO.OUT)
        GPIO.output(self.led1_pin, self.off)
        GPIO.output(self.led2_pin, self.off)
        GPIO.output(self.red_pin, self.off)
        GPIO.output(self.green_pin, self.off)
        GPIO.output(self.blue_pin, self.off)

    def _set_pin(self, pin, value='on'):
        GPIO.output(pin, self.on if value == 'on' else self.off)

    def set_led1(self, *args):
        self._set_pin(self.led1_pin, *args)

    def set_led2(self, *args):
        self._set_pin(self.led2_pin, *args)

    def set_red(self, *args):
        self._set_pin(self.red_pin, *args)

    def set_green(self, *args):
        self._set_pin(self.green_pin, *args)

    def set_blue(self, *args):
        self._set_pin(self.blue_pin, *args)
