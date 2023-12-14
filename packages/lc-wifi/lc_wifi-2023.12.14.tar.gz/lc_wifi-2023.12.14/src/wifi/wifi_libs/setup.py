from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="wifi_utils",
    version='0.3.0-rc.24',
    license="MIT",
    platforms=["any"],
    description="Set of tools for wifi optimization",
    py_modules=['baseG2', 'baseG5', 'ch_5G', 'BruteForceG2', 'BruteForceG5', 'MetaGreedy'],
    url='https://devel.tr069.ru:9090/wifi/wifi-libs',
    author='Vladimir Fadeev',
    author_email='vladimir.fadeev@tr069.cloud',
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
