import subprocess
import sys
from setuptools import setup, find_packages
from setuptools.command.install import install

class CheckEnvVariables(install):
    def run(self):
        # Run the environment variable check before installing
        subprocess.check_call([sys.executable, 'axya_whisper/check.py'])
        super().run()

setup(
    name='axya-whisper',
    version='0.1.39',
    packages=find_packages(),
    package_data={'': ['assets/axya.ico']},
    install_requires=[
        'pywin32',
        'keyring',
        'requests',
        'pystray',
        'Pillow'
    ],
    cmdclass={'install': CheckEnvVariables},
    entry_points={
        'console_scripts': [
            'axya-whisper-windows-service=axya_whisper.service:main',
        ],
    },
    python_requires='>=3.6',
)