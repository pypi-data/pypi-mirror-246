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

from axya_whisper.main import main

print("HMMMM...")

class HelloWindowService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'AxyaWhisperService'
    _svc_display_name_ = 'Axya Genius Whisper'

    def __init__(self, args):
        print("Running AxyaWhisper for Genius ERP")
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.icon = None
        socket.setdefaulttimeout(5)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.icon:
           self.icon = self.create_system_tray_icon()


    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))
        self.run_service()

    def create_system_tray_icon(self):
       menu = Menu(MenuItem('Exit', self.on_exit))
       icon = Icon("MyIcon", "axya.ico", menu=menu)
       icon.run()
       return icon
    
    def on_exit(self, icon, item):
       icon.stop()

    def run_service(self):
        self.icon = self.create_system_tray_icon()
        while True:
            try:
                if "--status" in sys.argv:
                    print("The service is running...")
                else:
                    print("Getting here")
                    try:
                        main()
                    except Exception as e:
                        print(f"Error running main: {e}")

                time.sleep(60)

            except Exception as e:
                servicemanager.LogErrorMsg(str(e))
                time.sleep(300)

