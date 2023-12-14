from setuptools import setup, find_packages

setup(
    name='openmeter_client',
    version='0.0.1',
    description='A Python client to interact with the OpenMeter API endpoints',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        "requests",
        "pandas",
        "loguru",
    ],
)