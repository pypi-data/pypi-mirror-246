from setuptools import setup, find_packages

setup(
    name='axya-whisper',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pywin32',
    ],
    entry_points={
        'console_scripts': [
            'axya-whisper-window-service = axya_whisper.service:main',
        ],
    },
    python_requires='>=3.6',
)
