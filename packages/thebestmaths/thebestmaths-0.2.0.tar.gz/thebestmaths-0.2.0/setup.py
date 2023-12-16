from setuptools import setup, find_packages


with open('README.md', 'r') as f:
    desc = f.read()

setup(
    name='thebestmaths',
    version='0.2.0',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='Torrez',
    requires=[
        'bestErrors(>=0.3.0)'
    ],
    packages=find_packages()
)