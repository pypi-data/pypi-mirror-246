from setuptools import setup, find_packages

setup(
    name='openmeter_client',
    version='0.0.1-alpha0',
    description='A Python client to interact with the OpenMeter API endpoints',
    packages=find_packages(where='openmeter'),
    package_dir={'': 'openmeter'},
    install_requires=[
        "requests",
        "pandas",
        "loguru",
    ],
    package_data={
        '': ['docs/*'],
    },
)