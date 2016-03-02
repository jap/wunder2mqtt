from distutils.core import setup

version = '0.1'

setup(name='wunder2mqtt',
      version=version,
      packages=['wunder2mqtt'],
      install_requires=[
          'paho-mqtt>=1.1,<1.2',
          'requests>=2.9.1,<2.10',
          'PyYAML>=3.11,<3.12'
      ],
      entry_points = {
          'console_scripts': ['wunder2mqtt=wunder2mqtt.main:main']
      }
     )
