import os
import re

from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


def get_version(package):
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    packages = []
    for dirpath, dirnames, filenames in os.walk(package):
        if os.path.exists(os.path.join(dirpath, '__init__.py')):
            packages.append(dirpath)
    return packages


def get_package_data(package):
    filepaths = []
    for dirpath, dirnames, filenames in os.walk(package):
        if os.path.exists(os.path.join(dirpath, '__init__.py')):
            continue

        base = dirpath.replace(package + os.sep, '', 1)
        for filename in filenames:
            filepaths.append(os.path.join(base, filename))

    return {package: filepaths}


setup(name='devicehive_webconfig',
      version=get_version('devicehive_webconfig'),
      author='DataArt (http://dataart.com)',
      author_email='info@devicehive.com',
      url='https://devicehive.com',
      license='Apache License 2.0',
      description='DeviceHive Python web configurator',
      long_description=long_description,
      keywords='iot cloud m2m gateway embedded devicehive configurator web ui',
      packages=get_packages('devicehive_webconfig'),
      package_data=get_package_data('devicehive_webconfig'),
      install_requires=['devicehive>=2.1.3', 'six>=1.11.0'],
      python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: MacOS',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Home Automation',
          'Topic :: Internet',
          'Topic :: Software Development :: Embedded Systems',
      ])
