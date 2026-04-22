import winreg
import os

computerName =os.getenv('COMPUTERNAME')

winreg.ConnectRegistry(None, "HKEY_CURRENT_USER")

# winreg.LoadKey(key, sub_key, file_name)
# HKEY_CURRENT_USER\Software\VB and VBA Program Settings\Shortcut Tool\Stored Values\errorInCh