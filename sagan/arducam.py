import subprocess
from collections import namedtuple
from datetime import datetime

CAPTURE_EXECUTABLE = 'ov2640_capture'
X_RESOLUTION = 800
Y_RESOLUTION = 600

CameraCaptureResult = namedtuple(
    'CameraCaptureResult',
    'filename'
)


class Camera:
    def capture(self, filename=None):

        if not filename:
            filename = '{}.jpg'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))

        if len(filename) > 4 and filename[-4:] != '.jpg':
            filename += '.jpg'

        command = '{} -c {} {}x{}'.format(
            CAPTURE_EXECUTABLE,
            filename,
            X_RESOLUTION,
            Y_RESOLUTION
        )
        status = subprocess.call(command, shell=True)
        assert status == 0, "Failed to capture image with command {}".format(command)
        return CameraCaptureResult(filename)
