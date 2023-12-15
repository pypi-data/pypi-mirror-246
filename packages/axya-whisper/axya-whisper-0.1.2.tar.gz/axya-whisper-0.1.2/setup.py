# setup.py

from setuptools import setup, find_packages

setup(
    name='axya-whisper',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'pywin32',
        'keyring',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'axya-whisper-windows-service=axya_whisper.__main__:main',
        ],
    },
    python_requires='>=3.6',
)
