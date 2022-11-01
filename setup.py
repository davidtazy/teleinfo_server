from setuptools import setup

setup(name='funniest',
      version='0.1',
      description='teleinfo module',
      url='',
      author='davidtazy',
      author_email='',
      license='MIT',
      packages=['teleinfo'],
      install_requires=[
          'influxdb-client','pySerial'
      ],
      entry_points = {
        'console_scripts': ['teleinfo=teleinfo.__main__:main'],
      },
      zip_safe=False)