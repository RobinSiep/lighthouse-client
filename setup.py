from setuptools import setup


requires = [
    'psutil',
    'python-socketio'
]

setup(
    name='sauronclient',
    version='0.1',
    author='Robin Siep',
    author_email='hello@robinsiep.dev',
    install_requires=requires
)
