# service.py

import os
import sys
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from pystray import Icon, Menu, MenuItem
from PIL import Image
from axya_whisper.main import service
from axya_whisper.upgrade import upgrade_and_restart_service

class HelloWindowService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'AxyaWhisperService'
    _svc_display_name_ = 'Axya Genius Whisper'
    _svc_description_ = "A service to sync GeniusERP with Axya."
    _svc_start_type_ = win32service.SERVICE_AUTO_START

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.icon = None
        self.is_alive = True

        socket.setdefaulttimeout(5)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = True
        if self.icon:
            self.icon.stop()

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.run_service()

    def create_system_tray_icon(self):
        menu = Menu(MenuItem('Exit', self.on_exit))
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "assets/axya.ico")
        image = Image.open(icon_path)
        icon = Icon("MyIcon", image, menu=menu)
        icon.run()
        return icon

    def on_exit(self, icon, item):
        self.SvcStop()
        
    def run_service(self):
        self.icon = self.create_system_tray_icon()
        self.whisper()
    
    def whisper(self):
        while self.is_alive:
            service()

def main():
    win32serviceutil.HandleCommandLine(HelloWindowService)

if __name__ == '__main__':
    main()
