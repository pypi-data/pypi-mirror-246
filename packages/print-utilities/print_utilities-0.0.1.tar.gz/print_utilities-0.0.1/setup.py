from setuptools import setup, find_packages

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='print_utilities',
    version='0.0.1',
    license='MIT License',
    author='CarlosAllberto',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='dasilvacarlosalberto344@gmail.com',
    keywords='print utilities',
    description='Uma biblioteca com varias utilidades para printar',
    packages=find_packages(),)