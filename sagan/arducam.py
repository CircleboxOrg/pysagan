import subprocess
from .telemetry import Telemetry
from collections import namedtuple
from datetime import datetime
import base64
import json

CAPTURE_EXECUTABLE = 'ov2640_capture'
X_RESOLUTION = 1600
Y_RESOLUTION = 1200

CameraCaptureResult = namedtuple(
    'CameraCaptureResult',
    'filename'
)


class Camera:

    def _image_to_string(self, filename=None):
        if filename is not None:
            try:
                with open(filename, 'rb') as imgText:
                    result = "START_BASE_64{}END_BASE_64".format(base64.encodebytes(imgText.read()))
                    return result
            except FileNotFoundError:
                pass
        return ""

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
        packet = {
            "src": self._image_to_string(filename)
        }
        Telemetry.update("cam", packet)
        camera_result = CameraCaptureResult(filename)
        assert status == 0, "Failed to capture image with command {}".format(command)
        return camera_result
