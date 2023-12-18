from setuptools import setup


setup(
    name='conson',
    version='2.1',
    description='A simple json configuration file manager',
    long_description='./README.md',
    author='Paweł Gabryś',
    author_email='p.gabrys@int.pl',
    packages=['conson'],
    install_requires=['cryptography>=41.0.3'],
)
