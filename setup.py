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


def get_requires():
    with open('requirements.txt') as f:
        return f.readlines()


setup(name='devicehive-webconfig',
      version=get_version('dh_webconfig'),
      author='DataArt (http://dataart.com)',
      author_email='info@devicehive.com',
      url='https://devicehive.com',
      license='Apache License 2.0',
      description='DeviceHive Python web configurator',
      long_description=long_description,
      keywords='iot cloud m2m gateway embedded devicehive configurator web ui',
      packages=get_packages('dh_webconfig'),
      package_data=get_package_data('dh_webconfig'),
      install_requires=get_requires()
      )
