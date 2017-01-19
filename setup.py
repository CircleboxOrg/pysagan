from distutils.core import setup

setup(
    name='sagan',
    version='',
    packages=['sagan'],
    requires=['smbus-cffi', 'RPIO'],
    url='www.cuberider.com',
    license='',
    author='T A H Smith, A W Collins',
    author_email='sagan@cuberider.com',
    description='Python library for interfacing with sagan board'
)
