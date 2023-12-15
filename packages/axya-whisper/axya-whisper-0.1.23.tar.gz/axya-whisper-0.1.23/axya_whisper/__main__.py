import os
import sys
import time
import win32serviceutil
import win32service
import win32event

from .service import HelloWindowService
def main():
    print("Executing main..")
   # Remove the following line, as it might be interfering with console execution
    # HelloWindowService.parse_command_line()
    win32serviceutil.HandleCommandLine(HelloWindowService)
    print("win32serviceutil.HandleCommandLine(HelloWindowService)")