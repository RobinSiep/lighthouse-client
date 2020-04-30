from setuptools import setup


requires = [
    'aiohttp',
    'netifaces',
    'psutil',
    'python-socketio',
    'requests'
]

setup(
    name='lighthouseclient',
    version='0.1',
    author='Robin Siep',
    author_email='hello@robinsiep.dev',
    install_requires=requires
)
