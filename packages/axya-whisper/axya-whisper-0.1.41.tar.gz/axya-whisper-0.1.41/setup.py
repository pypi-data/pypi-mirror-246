import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install


setup(
    name='axya-whisper',
    version='0.1.41',
    packages=find_packages(),
    package_data={'': ['assets/axya.ico']},
    install_requires=[
        'pywin32',
        'keyring',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'axya-whisper=axya_whisper.main:service',
        ],
    },
    python_requires='>=3.6',
)