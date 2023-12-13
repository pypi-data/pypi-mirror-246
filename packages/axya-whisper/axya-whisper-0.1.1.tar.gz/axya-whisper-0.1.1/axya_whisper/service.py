import os
import sys
import subprocess
import time
import win32serviceutil
import win32service
import win32event
import servicemanager
import socket

from hello_window_service.main import main

class HelloWindowService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'AxyaWhisperService'
    _svc_display_name_ = 'Axya Genius Whisper'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(5)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        while True:
            try:
                # Load configuration
                token = os.getenv('AXYA_API_SERVICE_TOKEN', '')
                main(token)

                # Sleep for 5 minutes (adjust as needed)
                time.sleep(300)

            except Exception as e:
                servicemanager.LogErrorMsg(str(e))
                time.sleep(300)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(HelloWindowService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(HelloWindowService)
