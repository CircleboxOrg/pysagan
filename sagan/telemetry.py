_FIFO = open('/tmp/sagan_telemetry', 'w')


class Telemetry:

    @staticmethod
    def update(prefix: str, data: str):
        try:
            _FIFO.write("{}:{}\n".format(prefix, data.replace('"', '\\"')))
            _FIFO.flush()
        except:
            return False
        return True
