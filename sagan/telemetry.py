_FIFO = open('/tmp/sagan', 'w')


class Telemetry:

    @staticmethod
    def update(prefix: str, data: str):
        try:
            _FIFO.write("{}:{}".format(prefix, data))
        except:
            return False
        return True
