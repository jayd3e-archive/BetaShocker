#BetaShock/setup.py
import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGES')).read()

entry_points = """
      [paste.app_factory]
      main = betashock:main
      """

requires = ['pyramid',
            'pyramid_tm',
            'pyramid_debugtoolbar',
            'sqlalchemy',
            'mako',
            'deform']

setup(name='BetaShock',
      version='0.1dev',
      description='',
      long_description=README + '\n\n' + CHANGES,
      install_requires=requires,
      url='http://localhost',
      packages=['betashock'],
      test_suite='betashock.tests',
      entry_points = entry_points
)
