import subprocess
from .telemetry import Telemetry
from collections import namedtuple
from datetime import datetime

CAPTURE_EXECUTABLE = 'ov2640_capture'
X_RESOLUTION = 1600
Y_RESOLUTION = 1200

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
        camera_result = CameraCaptureResult(filename)

        #todo - send image through telemetry
        assert status == 0, "Failed to capture image with command {}".format(command)
        return camera_result
