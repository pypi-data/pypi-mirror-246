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
        print("here we go again")
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.icon = self.create_system_tray_icon()
        socket.setdefaulttimeout(5)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.icon = self.create_system_tray_icon()


    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))

        if len(sys.argv) == 1:
            servicemanager.LogMsg(
                servicemanager.EVENTLOG_INFORMATION_TYPE,
                servicemanager.PYS_SERVICE_STARTED,
                (self._svc_name_, '')
            )
            self.run_service()
        else:
            win32serviceutil.HandleCommandLine(self)

    def create_system_tray_icon(self):
       menu = Menu(MenuItem('Exit', self.on_exit))
       icon = Icon("MyIcon", "axya.ico", menu=menu)
       icon.run()
       return icon
    def run_service(self):
        while True:
            try:
                if "--status" in sys.argv:
                    print("Service is in status mode.")
                else:
                    print("Getting here")
                    main()

                # Sleep for 5 minutes (adjust as needed)
                time.sleep(300)

            except Exception as e:
                servicemanager.LogErrorMsg(str(e))
                time.sleep(300)

