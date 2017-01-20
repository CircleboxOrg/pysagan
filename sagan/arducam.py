import subprocess
import os

CAPTURE_EXECUTABLE = 'ov2640_capture'
X_RESOLUTION = 800
Y_RESOLUTION = 600


class Camera:
    def capture(self, filename='image.jpg'):
        if (not len(filename) > 4) and filename[-4:] != '.jpg':
            filename += '.jpg'

        path = os.path.join(os.curdir, filename)
        command = '{} -c {} {}x{}'.format(
            CAPTURE_EXECUTABLE,
            path,
            X_RESOLUTION,
            Y_RESOLUTION
        )
        status = subprocess.call(command, shell=True)
        assert status == 0, "Failed to capture image with command {}".format(command)
        return path
