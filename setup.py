from setuptools import setup

setup(name='ebay items manager',
      version='0.1.0',
      packages=['app'],
      entry_points={
          'console_scripts': [
              'ebaycli = app.app:start'
          ]
      },
      )