# setup.py

from setuptools import setup, find_packages

setup(
    name='axya-whisper',
    version='0.1.24',
    packages=find_packages(),
    package_data={'': ['assets/axya.ico']},
    install_requires=[
        'pywin32',
        'keyring',
        'requests',
        'pystray',
        'Pillow'
    ],
    entry_points={
        'console_scripts': [
            'axya-whisper-windows-service=axya_whisper.__main__:main',
        ],
    },
    python_requires='>=3.6',
)
