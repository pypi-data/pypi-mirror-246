from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    desc = f.read()

setup(
    name='thebestmaths',
    version='0.1.0',
    long_description=desc,
    author='Torrez',
    requires=[
        'bestErrors'
    ],
    packages=find_packages()
)