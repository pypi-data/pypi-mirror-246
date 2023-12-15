import subprocess
import sys
import win32serviceutil

def upgrade_and_restart_service(service_name):
    try:
        # Upgrade axya-whisper package using pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "axya-whisper"])

        # Check if the package was upgraded
        # You might need to replace 'axya-whisper' with the actual package name
        package_version = subprocess.check_output([sys.executable, "-m", "pip", "show", "axya-whisper"])
        package_version = package_version.decode("utf-8")
        current_version = None

        for line in package_version.split('\n'):
            if line.startswith('Version:'):
                current_version = line.split(' ')[-1].strip()
                break

        if current_version:
            print(f"axya-whisper upgraded to version {current_version}")
            restart_service(service_name)
        else:
            print("axya-whisper is already up-to-date")

    except subprocess.CalledProcessError as e:
        print(f"Error upgrading axya-whisper: {e}")

def restart_service(service_name):
    try:
        win32serviceutil.RestartService(service_name)
        print(f"The service '{service_name}' has been restarted.")
    except Exception as e:
        print(f"Error restarting service: {e}")

