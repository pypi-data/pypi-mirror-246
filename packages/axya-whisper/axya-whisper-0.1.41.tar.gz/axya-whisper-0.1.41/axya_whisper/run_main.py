import subprocess
import sys

subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "axya-whisper"])

from axya_whisper import main

def run():
    main.service()

if __name__ == "__main__":
    run()