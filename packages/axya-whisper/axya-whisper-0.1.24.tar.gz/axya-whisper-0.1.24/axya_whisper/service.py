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
from axya_whisper.main import main
from axya_whisper.upgrade import upgrade_and_restart_service

def check_environment_variables(self):
    required_variables = [
        'GENIUS_API_URL',
        'GENIUS_API_LOGIN',
        'GENIUS_API_PASSWORD',
        'GENIUS_API_COMPANY_CODE',
        'AXYA_API_URL',
        'AXYA_API_TOKEN',
    ]

    for variable in required_variables:
        if not os.environ.get(variable):
            print(f"!!!Environment variable {variable} is not set. Please set it and restart the service.!!!!")
            sys.exit(1)

class HelloWindowService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'AxyaWhisperService'
    _svc_display_name_ = 'Axya Genius Whisper'
    _svc_description_ = "A service to sync the GeniusERP with Axya."
    _svc_start_type_ = win32service.SERVICE_AUTO_START


    def __init__(self, args):
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
       script_dir = os.path.dirname(os.path.abspath(__file__))
       icon_path = os.path.join(script_dir, "assets/axya.ico")
       image = Image.open(icon_path)
       icon = Icon("MyIcon", image, menu=menu)
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
                        print("checking for updates...")
                        upgrade_and_restart_service(self._svc_name_)
                        print("Running main...")
                        main()
                    except Exception as e:
                        print(f"Error running main: {e}")

                time.sleep(60)

            except Exception as e:
                servicemanager.LogErrorMsg(str(e))
                time.sleep(300)

