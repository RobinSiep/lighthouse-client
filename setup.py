from setuptools import setup


requires = [
    'aiohttp',
    'netifaces',
    'psutil',
    'python-socketio[asyncio_client]',
    'requests'
]

setup(
    name='lighthouseclient',
    version='0.1',
    author='Robin Siep',
    author_email='hello@robinsiep.dev',
    install_requires=requires,
    entry_points={
        'console_scripts': [
            "lighthouseclient = lighthouseclient.app:main"
        ]
    }
)
