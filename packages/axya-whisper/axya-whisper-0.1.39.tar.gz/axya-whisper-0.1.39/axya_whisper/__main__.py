import os
import sys
import time
import win32serviceutil
import win32service
import win32event

from .service import HelloWindowService

def main():
    win32serviceutil.HandleCommandLine(HelloWindowService)