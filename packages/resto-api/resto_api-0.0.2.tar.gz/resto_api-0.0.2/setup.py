from setuptools import find_packages, setup

setup(
    name='resto_api',
    packages=find_packages(include=['rapid']),
    version='0.0.2',
    description='resto python API',
    author='Jérôme Gasperi',
    install_requires=[
        "requests"
    ]
)